import click
import time
import pprint
import numpy as np
import pickle
import matplotlib
import matplotlib.pyplot as plt

from utils import compute_room_irs, RoomSimSoftware

font = {"family": "Times New Roman", "weight": "normal", "size": 18}
matplotlib.rc("font", **font)


def plot_results(software, ism_order_vals, proc_time, proc_time_std, n_std):
    markers = ["o", "^", "v", "x", ">", "<", "D", "+"]
    plt.figure()
    for i, _software in enumerate(software):
        _proc_time = []
        _proc_time_std = []
        for ism_order in ism_order_vals:
            if _software in proc_time[ism_order].keys():
                _proc_time.append(proc_time[ism_order][_software])
                _proc_time_std.append(proc_time_std[ism_order][_software])
            else:
                break
        _proc_time = np.array(_proc_time)
        _proc_time_std = np.array(_proc_time_std)
        plt.plot(
            ism_order_vals[: len(_proc_time)],
            _proc_time,
            label=_software,
            marker=markers[i],
        )
        ax = plt.gca()
        ax.fill_between(
            ism_order_vals[: len(_proc_time)],
            (_proc_time - n_std * _proc_time_std),
            (_proc_time + n_std * _proc_time_std),
            alpha=0.2,
        )

    plt.legend(loc="upper left")
    plt.xlabel("Specular depth / ISM order")
    plt.ylabel("Processing time (s)")
    plt.grid()
    plt.tight_layout()
    ax = plt.gca()
    ax.set_xticks(ism_order_vals)
    plt.savefig("ism.png")


@click.command()
@click.option("--n_trials", type=int, default=100)
@click.option("--pickle_path", type=str, default=None)
def profile_room_gen(n_trials, pickle_path):
    """
    Parameters
    ----------
    n_trials : int
        How many trials to average over. Ignored if `pickle_path` is provided.
    pickle_path : str
        File path to already computed results in order to plot them.
    """

    if pickle_path is None:
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

        # sweep number of rays
        ism_order_vals = [2, 3, 4, 5, 6, 7]
        n_rays = int(1e4)
        proc_time = dict()
        proc_time_std = dict()
        for ism_order in ism_order_vals:

            print("ISM order : {}".format(ism_order))
            proc_time[ism_order] = dict()
            proc_time_std[ism_order] = dict()

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
                        ray_tracing_param=ray_tracing_param,
                    )
                    timing.append(time.time() - start_time)
                proc_time[ism_order][_software] = np.mean(timing)
                proc_time_std[ism_order][_software] = np.std(timing)
                print(
                    "{} : {} seconds".format(
                        _software, proc_time[ism_order][_software]
                    )
                )

        pprint.pprint(proc_time)
        pprint.pprint(proc_time_std)

        data = {
            "proc_time": proc_time,
            "proc_time_std": proc_time_std,
            "ism_order_vals": ism_order_vals,
            "software": software,
            "n_std": n_std,
            "n_rays": n_rays,
            "n_trials": n_trials,
        }

        with open("profile_ism_order.pickle", "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:

        with open(pickle_path, "rb") as f:
            data = pickle.load(f)

        software = data["software"]
        ism_order_vals = data["ism_order_vals"]
        proc_time = data["proc_time"]
        proc_time_std = data["proc_time_std"]
        n_std = data["n_std"]

    # plot results
    plot_results(software, ism_order_vals, proc_time, proc_time_std, n_std)


if __name__ == "__main__":
    profile_room_gen()
