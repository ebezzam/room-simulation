import click
import time
import numpy as np
import pprint
import matplotlib
import matplotlib.pyplot as plt

from utils import compute_room_irs, RoomSimSoftware

font = {"family": "Helvetica", "weight": "normal", "size": 18}
matplotlib.rc("font", **font)


@click.command()
@click.argument("n_trials", type=int, default=100)
def profile_room_gen(n_trials):
    print(
        "\nCOMPARING ROOM SIMULATION SOFTWARE WITH {} TRIALS\n".format(
            n_trials
        )
    )

    software = [
        RoomSimSoftware.PYGSOUND,
        RoomSimSoftware.PYROOMACOUSTICS,
    ]
    n_std = 1

    markers = ["o", "^", "v", "x", ">", "<", "D", "+"]

    # sweep number of rays
    n_ray_vals = np.array([1e3, 3e3, 1e4, 3e4, 1e5], dtype=int)
    ism_order = 3
    proc_time = dict()
    proc_time_std = dict()
    for n_rays in n_ray_vals:

        print("number of rays : {}".format(n_rays))
        proc_time[n_rays] = dict()
        proc_time_std[n_rays] = dict()

        # loop through software
        for _software in software:
            ray_tracing_param = None

            if _software == RoomSimSoftware.PYGSOUND:
                ray_tracing_param = {
                    "diffuse_count": int(n_rays),
                    "specular_count": 6 ** ism_order,
                    "specular_depth": ism_order,
                }
            elif _software == RoomSimSoftware.PYROOMACOUSTICS:
                ray_tracing_param = {"n_rays": int(n_rays)}
            assert ray_tracing_param is not None

            timing = []
            for _ in range(n_trials):
                start_time = time.time()
                compute_room_irs(
                    room_dim=[8, 9, 3],
                    room_properties=0.5,  # rt60
                    scattering=0.5,
                    ism_order=ism_order
                    if _software == RoomSimSoftware.PYROOMACOUSTICS
                    else None,
                    mic_pos=[0.3, 3, 0.2],
                    source_pos=[[3.2, 3, 1.8]],
                    software=_software,
                    ray_tracing=True,
                    ray_tracing_param=ray_tracing_param,
                )
                timing.append(time.time() - start_time)
            proc_time[n_rays][_software] = np.mean(timing)
            proc_time_std[n_rays][_software] = np.std(timing)
            print(
                "{} : {} seconds".format(
                    _software, proc_time[n_rays][_software]
                )
            )

    pprint.pprint(proc_time)
    pprint.pprint(proc_time_std)

    # plot results
    plt.figure()
    for i, _software in enumerate(software):
        _proc_time = []
        _proc_time_std = []
        for n_rays in n_ray_vals:
            _proc_time.append(proc_time[n_rays][_software])
            _proc_time_std.append(proc_time_std[n_rays][_software])
        _proc_time = np.array(_proc_time)
        _proc_time_std = np.array(_proc_time_std)

        plt.loglog(n_ray_vals, _proc_time, label=_software, marker=markers[i])
        ax = plt.gca()
        ax.fill_between(
            n_ray_vals,
            (_proc_time - n_std * _proc_time_std),
            (_proc_time + n_std * _proc_time_std),
            alpha=0.2,
        )

    plt.legend()
    plt.xlabel("Number of rays")
    plt.ylabel("Processing time [s]")
    plt.grid()
    plt.tight_layout()
    plt.savefig("number_rays.png")


if __name__ == "__main__":
    profile_room_gen()
