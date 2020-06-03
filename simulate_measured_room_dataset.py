import os
import json
import shutil
import click
import argparse
import soundfile as sf
from pprint import pprint

from utils import (
    get_subdirectories,
    compute_room_irs,
    RoomSimSoftware,
)
from room import Room, WallRegistry

"""
Copy a measured room bundle by copying its parameters such as:
- room dimensions
- source / microphone positions
- reverberation property / materials
- temperature (for air absorption)

Example with ISM order 17 using `pyroomacoustics`.
```
python simulate_measured_room_dataset.py \
measured_room_dataset_train_BUT_ReverbDB_7rooms_2020_05_07T15_23_53
```

Example with `pygsound`.
```
python simulate_measured_room_dataset.py \
measured_room_dataset_dev_BUT_ReverbDB_2rooms_2020_05_07T15_23_53 \
--software pygsound
```
"""


room_materials_registry = {
    # train
    "VUT_FIT_C236": {
        WallRegistry.CEILING: "hard_surface",
        WallRegistry.FLOOR: "ceramic_tiles",
        WallRegistry.EAST: "hard_surface",
        WallRegistry.WEST: "hard_surface",
        WallRegistry.NORTH: "hard_surface",
        WallRegistry.SOUTH: "glass_window",
    },
    "Hotel_SkalskyDvur_ConferenceRoom2": {
        WallRegistry.CEILING: "plywood",
        WallRegistry.FLOOR: "thin_carpet",
        WallRegistry.EAST: "hard_surface",
        WallRegistry.WEST: "hard_surface",
        WallRegistry.NORTH: "hard_surface",
        WallRegistry.SOUTH: "cotton_cloth",
    },
    "VUT_FIT_E112": {
        WallRegistry.CEILING: "plasterboard",
        WallRegistry.FLOOR: "thin_carpet",
        WallRegistry.EAST: "vertical_blinds",
        WallRegistry.WEST: "smooth_concrete",
        WallRegistry.NORTH: "plywood",
        WallRegistry.SOUTH: "plywood",
    },
    "VUT_FIT_L207": {
        WallRegistry.CEILING: "smooth_concrete",
        WallRegistry.FLOOR: "hard_surface",
        WallRegistry.EAST: "plasterboard",
        WallRegistry.WEST: "plasterboard",
        WallRegistry.NORTH: "glass_window",
        WallRegistry.SOUTH: "smooth_concrete",
    },
    "VUT_FIT_L227": {
        WallRegistry.CEILING: "smooth_concrete",
        WallRegistry.FLOOR: "ceramic_tiles",
        WallRegistry.EAST: "smooth_concrete",
        WallRegistry.WEST: "smooth_concrete",
        WallRegistry.NORTH: "smooth_concrete",
        WallRegistry.SOUTH: "smooth_concrete",
    },
    "VUT_FIT_Q301": {
        WallRegistry.CEILING: "plasterboard",
        WallRegistry.FLOOR: "thin_carpet",
        WallRegistry.EAST: "plasterboard",
        WallRegistry.WEST: "plasterboard",
        WallRegistry.NORTH: "glass_window",
        WallRegistry.SOUTH: "plasterboard",
    },
    "Hotel_SkalskyDvur_Room112": {
        WallRegistry.CEILING: "smooth_concrete",
        WallRegistry.FLOOR: "thin_carpet",
        WallRegistry.EAST: "hard_surface",
        WallRegistry.WEST: "hard_surface",
        WallRegistry.NORTH: "curtains_hung",
        WallRegistry.SOUTH: "hard_surface",
    },
    # dev
    "VUT_FIT_D105": {
        WallRegistry.CEILING: "plasterboard",
        WallRegistry.FLOOR: "plywood",
        WallRegistry.EAST: "smooth_concrete",
        WallRegistry.WEST: "smooth_concrete",
        WallRegistry.NORTH: "plywood",
        WallRegistry.SOUTH: "smooth_concrete",
    },
    "VUT_FIT_L212": {
        WallRegistry.CEILING: "smooth_concrete",
        WallRegistry.FLOOR: "hard_surface",
        WallRegistry.EAST: "glass_window",
        WallRegistry.WEST: "plasterboard",
        WallRegistry.NORTH: "plasterboard",
        WallRegistry.SOUTH: "plasterboard",
    },
}


def simulate_measured_bundle(
    original_dataset,
    air_abs=False,
    ism_order=17,
    ray_tracing=False,
    freq_dep=False,
    software=RoomSimSoftware.PYROOMACOUSTICS,
):
    if software == RoomSimSoftware.PYGSOUND:
        ism_order = None
        air_abs = False
        freq_dep = False
        ray_tracing = True

    ray_tracing_param = None
    if ray_tracing:
        if software == RoomSimSoftware.PYROOMACOUSTICS:
            ray_tracing_param = {
                "n_rays": int(1e5),
                "receiver_radius": 0.5,
                "time_thres": 10.0,
                # "energy_thres": 1e-7,
                # "hist_bin_size": 0.004
            }
        elif software == RoomSimSoftware.PYGSOUND:
            ray_tracing_param = {
                "diffuse_count": 20000,
                "specular_count": 2000,
                "src_radius": 0.01,
                "mic_radius": 0.01,
            }

    # load dataset
    with open(
        os.path.join(original_dataset, "dataset_metadata.json")
    ) as json_file:
        metadata = json.load(json_file)

    n_rooms = metadata["n_rooms"]
    dataset_type = metadata["dataset_type"]
    timestamp = metadata["timestamp"]

    # create output dir
    if ray_tracing and ism_order is not None and ism_order >= 0:
        sim_type = f"hyb{ism_order}"
    elif ray_tracing:
        sim_type = f"srt"
    else:
        sim_type = f"ism{ism_order}"
    if air_abs:
        sim_type += "_air_abs"
    if freq_dep:
        sim_type += "_freq_dep"
    dataset_id = (
        f"measured_room_dataset_SIM_{software}_{sim_type}"
        f"_{dataset_type}_{n_rooms}rooms_{timestamp}"
    )
    if os.path.isdir(dataset_id):
        click.confirm(
            "\n{} exists. Delete and replace?".format(dataset_id),
            default=True,
            abort=True,
        )
        shutil.rmtree(dataset_id)
    os.mkdir(dataset_id)
    data_index_file = "data_index.json"
    data_folder = "data"
    data_path = os.path.join(dataset_id, data_folder)
    print("New dataset ID : {}".format(dataset_id))
    os.mkdir(data_path)

    # loop through rooms
    original_data_folder = os.path.join(original_dataset, data_folder)
    rooms = get_subdirectories(original_data_folder)
    for k, _id in enumerate(rooms):

        original_room_subdir = os.path.join(original_data_folder, _id)
        room = Room.load(original_room_subdir)
        print("room {} / {} : {}".format(k + 1, n_rooms, room.id))

        # get room params
        room_params = room.params
        dimensions = room_params["dimensions"]
        temperature = room_params.get("temperature")

        # use furniture coverage as proxy for average scattering
        scattering = room_params.get("furniture_coverage", 0.5)
        scattering = max(scattering, 0.1)

        # get mic and speaker metadata, loop over
        speaker_metadata = room.speaker_metadata
        mic_metadata = room.mic_metadata

        speaker_pos = []
        for _speaker in speaker_metadata:
            speaker_pos.append(_speaker["target_location"])

        print("\nRoom params : ")
        pprint(room_params)

        print("speaker pos : ")
        print(speaker_pos)

        # create new room dir
        room_subdir = os.path.join(data_path, room.id)
        os.mkdir(room_subdir)
        rir_dir = os.path.join(room_subdir, "rir")
        os.mkdir(rir_dir)
        shutil.copy(
            os.path.join(original_room_subdir, "config.json"),
            os.path.join(room_subdir, "config.json"),
        )
        shutil.copytree(
            os.path.join(original_room_subdir, "background_noise"),
            os.path.join(room_subdir, "background_noise"),
        )

        for m, _mic in enumerate(mic_metadata):
            mic_subdir = os.path.join(rir_dir, "mic{}".format(m))
            os.mkdir(mic_subdir)

            mic_pos = _mic["mic_location"]
            print("    mic pos : {}".format(mic_pos))

            # estimate from impulse
            if freq_dep:
                materials = room_materials_registry[_id]
            else:
                materials = _mic["t60_estimate"]

            if isinstance(materials, list):
                # unique RT60 per mic-speaker pair
                mic_responses = []
                for spk_idx, rt60 in enumerate(materials):
                    resp, sample_rate = compute_room_irs(
                        room_dim=dimensions,
                        room_properties=rt60,
                        mic_pos=mic_pos,
                        source_pos=[speaker_pos[spk_idx]],
                        ism_order=ism_order,
                        ray_tracing_param=ray_tracing_param,
                        ray_tracing=ray_tracing,
                        air_absorption=air_abs,
                        temperature=temperature,
                        scattering=scattering,
                        software=software,
                    )
                    mic_responses += resp
            else:

                # compute RIR(s)
                mic_responses, sample_rate = compute_room_irs(
                    room_dim=dimensions,
                    room_properties=materials,
                    mic_pos=mic_pos,
                    source_pos=speaker_pos,
                    ism_order=ism_order,
                    ray_tracing_param=ray_tracing_param,
                    ray_tracing=ray_tracing,
                    air_absorption=air_abs,
                    temperature=temperature,
                    scattering=scattering,
                    software=software,
                )

            # write RIRs
            for n, _rir in enumerate(mic_responses):
                sf.write(
                    os.path.join(mic_subdir, "{}.wav".format(n)),
                    mic_responses[n],
                    sample_rate,
                )

    # write bundle metadata
    dataset_metadata = metadata.copy()
    dataset_metadata["dataset_id"] = dataset_id
    dataset_metadata["sim_type"] = sim_type
    output_json = os.path.join(dataset_id, "dataset_metadata.json")
    with open(output_json, "w") as f:
        json.dump(dataset_metadata, f, indent=4)

    # copy data index from measured dataset
    shutil.copy(
        src=os.path.join(original_dataset, data_index_file),
        dst=os.path.join(dataset_id, data_index_file),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy the configuration from a measured room dataset in"
        "simulation."
    )
    parser.add_argument(
        "dataset",
        type=str,
        default=None,
        help="Measured room dataset to copy.",
    )
    parser.add_argument(
        "--air_abs",
        action="store_true",
        help="Whether to take into account air absorption.",
    )
    parser.add_argument(
        "--ism",
        type=int,
        default=17,
        help="Image source method order, i.e. max number of wall reflections.",
    )
    parser.add_argument(
        "--rt",
        action="store_true",
        help="Whether to supplement with ray tracing simulation.",
    )
    parser.add_argument(
        "--freq_dep",
        action="store_true",
        help="Whether to be frequency dependent and use materials.",
    )
    parser.add_argument(
        "--software",
        type=str,
        default=RoomSimSoftware.PYROOMACOUSTICS,
        help="Simulation software to use.",
    )
    args = parser.parse_args()
    simulate_measured_bundle(
        original_dataset=args.dataset,
        air_abs=args.air_abs,
        ism_order=args.ism,
        ray_tracing=args.rt,
        freq_dep=args.freq_dep,
        software=args.software,
    )
