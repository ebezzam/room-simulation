import os
import pandas as pd
from pprint import pprint
import glob
import json
import datetime
import argparse

from utils import is_inside
from room import Room

"""
Example usage:
```
python create_measured_room_data_split.py \
/Volumes/Samsung_T5/BUT_ReverbDB_rel_19_06_RIR-Only 
```

Dataset can be downloaded here: 
https://speech.fit.vutbr.cz/software/but-speech-fit-reverb-database

"""


def create_measured_dataset(dataset_path, verbose=False):

    data_split = {
        "train": [
            # 1032 RIRs
            "VUT_FIT_L207",  # office, 6 speakers
            "VUT_FIT_Q301",  # office, 3 speakers
            "VUT_FIT_L227",  # staircase, 5 speakers
            "Hotel_SkalskyDvur_ConferenceRoom2",  # conference room, 4 speakers
            "VUT_FIT_E112",  # lecture room. 2 speakers
            "VUT_FIT_C236",  # meeting room, 10 speakers
            "Hotel_SkalskyDvur_Room112",  # hotel room, 5 speakers
        ],
        "dev": [
            # 280 RIRs
            "VUT_FIT_L212",  # office, 5 speakers
            "VUT_FIT_D105",  # lecture room, 6 speakers
        ],
    }
    data_index_file = "data_index.json"
    data_folder = "data"

    timestamp = str(datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%S"))
    # create each dataset
    for dataset_type in data_split.keys():

        print("\n----------------------------")
        print("\n{}".format(dataset_type.upper()))

        # get rooms for this split
        rooms = data_split[dataset_type]
        n_rooms = len(rooms)

        # create output dir
        dataset_id = "measured_room_dataset_{}_BUT_ReverbDB_{}rooms_{}".format(
            dataset_type, n_rooms, timestamp
        )
        os.mkdir(dataset_id)

        # loop through rooms
        n_rirs = 0
        data_index = []
        data_path = os.path.join(dataset_id, data_folder)
        os.mkdir(data_path)
        for _room in rooms:

            print("\n")
            print(_room)

            # extract room parameters, info can be found in "read_me.txt"
            room_params = dict()
            room_path = os.path.join(dataset_path, _room)
            room_metadata_path = os.path.join(room_path, "env_meta.txt")
            metadata = pd.read_csv(room_metadata_path, sep="\t", header=None)
            metadata.set_index(0, inplace=True)

            room_dim = [
                float(metadata.loc["$EnvWidth"][1]),
                float(metadata.loc["$EnvDepth"][1]),
                float(metadata.loc["$EnvHeight"][1]),
            ]
            room_params["dimensions"] = room_dim
            ceiling_materials = metadata.loc["$EnvMatCeiling"][1].lower()
            ceiling_materials = ceiling_materials.split(", ")
            room_params["ceiling_material"] = ceiling_materials

            floor_materials = metadata.loc["$EnvMatFloor"][1].lower()
            floor_materials = floor_materials.split(", ")
            room_params["floor_material"] = floor_materials

            wall_materials = metadata.loc["$EnvMatWall"][1].lower()
            wall_materials = wall_materials.split(", ")
            room_params["wall_material"] = wall_materials

            try:
                room_params["temperature"] = float(metadata.loc["$EnvTemp"][1])
            except:
                pass

            try:
                room_params["background_noise_level"] = float(
                    metadata.loc["$EnvBCKNoiseLevel"][1]
                )
            except:
                pass

            if _room == "VUT_FIT_C236":
                # doesn't have furniture coefficient but looks similar to
                # "VUT_FIT_L212" in pictures
                room_params["furniture_coverage"] = 0.75
            else:
                room_params["furniture_coverage"] = (
                    float(metadata.loc["$EnvFurniture"][1]) / 100
                )

            if verbose:
                pprint(room_params)

            # loop through speakers and extract RIRs and metadata
            recordings_path = os.path.join(room_path, "MicID01")
            speakers = next(os.walk(recordings_path))[1]
            # print("number of speakers : {}".format(len(speakers)))
            speaker_metadata = []
            responses = dict()
            mic_metadata = []
            background_noise = []
            _n_rir_room = 0
            valid_mic_idx = None
            for spk_idx, _speaker in enumerate(speakers):

                if valid_mic_idx is None:
                    # on first pass determine valid mics, i.e. those inside room
                    valid_mic_idx = []

                # extract speaker metadata
                _spk_metadata = dict()
                speaker_path = os.path.join(recordings_path, _speaker)
                speaker_metadata_path = os.path.join(
                    speaker_path, "spk_meta.txt"
                )
                metadata = pd.read_csv(
                    speaker_metadata_path, sep="\t", header=None
                )
                metadata.set_index(0, inplace=True)

                # speaker position
                speaker_pos = [
                    float(metadata.loc["$EnvSpk1Width"][1]),
                    float(metadata.loc["$EnvSpk1Depth"][1]),
                    float(metadata.loc["$EnvSpk1Height"][1]),
                ]

                # check if inside room
                if not is_inside(source_loc=speaker_pos, room_dim=room_dim):
                    print(
                        "speaker {} with position {} not inside room of "
                        "dimension {}, skipping...".format(
                            spk_idx, speaker_pos, room_dim
                        )
                    )
                    continue

                _spk_metadata["target_location"] = speaker_pos
                if verbose:
                    print("speaker : {}".format(_speaker))
                    pprint(_spk_metadata)
                speaker_metadata.append(_spk_metadata)

                mics = next(os.walk(speaker_path))[1]
                for mic_idx, _mic in enumerate(mics):

                    mic_path = os.path.join(speaker_path, _mic)

                    # extract mic metadata
                    metadata_path = os.path.join(mic_path, "mic_meta.txt")
                    metadata = pd.read_csv(
                        metadata_path, sep="\t", header=None
                    )
                    metadata.set_index(0, inplace=True)

                    # unique rt60 per mic-speaker pair
                    _mic_meta = dict()
                    mic_id = metadata.loc["$EnvMicID"][1]
                    rt60 = float(
                        metadata.loc["$EnvMic" + mic_id + "RelRT60"][1]
                    )

                    if spk_idx == 0:

                        ## -- Extract these parameters once
                        # mic position
                        mic_depth = float(
                            metadata.loc["$EnvMic" + mic_id + "Depth"][1]
                        )
                        mic_width = float(
                            metadata.loc["$EnvMic" + mic_id + "Width"][1]
                        )
                        mic_height = float(
                            metadata.loc["$EnvMic" + mic_id + "Height"][1]
                        )
                        mic_pos = [mic_width, mic_depth, mic_height]

                        # check if inside room
                        if not is_inside(
                            source_loc=mic_pos, room_dim=room_dim
                        ):
                            print(
                                "mic {} with position {} not inside room of "
                                "dimension {}, skipping...".format(
                                    mic_idx, mic_pos, room_dim
                                )
                            )
                            continue
                        valid_mic_idx.append(mic_idx)

                        _mic_meta["mic_location"] = mic_pos
                        _mic_meta["t60_estimate"] = [rt60]

                        if verbose:
                            print(_mic)
                            pprint(_mic_meta)
                        mic_metadata.append(_mic_meta)

                        # get background noise for mic
                        silence_path = glob.glob(
                            os.path.join(mic_path, "silence", "*.wav")
                        )[0]
                        background_noise.append(silence_path)

                        # get first RIR
                        rir_path = glob.glob(
                            os.path.join(mic_path, "RIR", "*.wav")
                        )[0]
                        responses[mic_idx] = [rir_path]

                    else:

                        if mic_idx not in valid_mic_idx:
                            # bad mic position, outside of room
                            continue

                        # add mic-speaker RT60
                        mic_metadata[valid_mic_idx.index(mic_idx)][
                            "t60_estimate"
                        ].append(rt60)

                        # merge other speakers response
                        rir_path = glob.glob(
                            os.path.join(mic_path, "RIR", "*.wav")
                        )[0]
                        responses[mic_idx].append(rir_path)

                    n_rirs += 1
                    _n_rir_room += 1

            responses = [responses[mic_idx] for mic_idx in valid_mic_idx]
            print(
                "number of VALID mics : {} / {}".format(
                    len(responses), len(mics)
                )
            )
            print(
                "number of VALID speakers : {} / {}".format(
                    len(responses[0]), len(speakers)
                )
            )

            # add to data index
            _data_index_entry = {
                "id": _room,
                "n_rir": _n_rir_room,
            }
            data_index.append(_data_index_entry)
            print("number of RIRs : {}".format(_n_rir_room))

            # save room
            room = Room(
                responses=responses,
                mic_metadata=mic_metadata,
                speaker_metadata=speaker_metadata,
                room_params=room_params,
                room_id=_room,
                background_noise=background_noise,
            )
            room.save(os.path.join(data_path, _room))

        # write bundle metadata and data index
        dataset_metadata = {
            "dataset_type": dataset_type,
            "timestamp": timestamp,
            "n_rooms": n_rooms,
            "n_rirs": n_rirs,
        }
        print("\nTOTAL number of RIRs : {}".format(n_rirs))
        output_json = os.path.join(dataset_id, "dataset_metadata.json")
        with open(output_json, "w") as f:
            json.dump(dataset_metadata, f, indent=4)

        output_json = os.path.join(dataset_id, data_index_file)
        with open(output_json, "w") as f:
            json.dump(data_index, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create measured room dataset from BUTReverbDB."
    )
    parser.add_argument(
        "path", type=str, default=None, help="Path to original dataset."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Whether to print a lot of info.",
    )
    args = parser.parse_args()
    create_measured_dataset(args.path, args.verbose)
