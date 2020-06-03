import click
import time
import pprint
import matplotlib
import matplotlib.pyplot as plt

from utils import compute_room_irs, RoomSimSoftware

font = {'family' : 'Helvetica',
        'weight' : 'normal',
        'size'   : 18}
matplotlib.rc('font', **font)


@click.command()
@click.argument("n_trials", type=int, default=100)
def profile_room_gen(n_trials):
    print(
        "\nCOMPARING ROOM SIMULATION SOFTWARE WITH {} TRIALS\n".format(n_trials)
    )

    software = [
        RoomSimSoftware.PYGSOUND,
        RoomSimSoftware.PYROOMACOUSTICS,
    ]

    markers = ['o', '^', 'v', 'x', '>', '<', 'D', '+']

    # sweep number of rays
    ism_order_vals = [2, 3, 4, 5, 6, 7]
    n_rays = int(1e4)
    proc_time = dict()
    for ism_order in ism_order_vals:

        print("ISM order : {}".format(ism_order))
        proc_time[ism_order] = dict()

        # loop through software
        for _software in software:
            ray_tracing_param = None

            if _software == RoomSimSoftware.PYGSOUND:
                ray_tracing_param = {
                    "diffuse_count": int(n_rays),
                    "specular_count": 6**ism_order,
                    "specular_depth": ism_order
                }
            elif _software == RoomSimSoftware.PYROOMACOUSTICS:
                ray_tracing_param = {
                    "n_rays": int(n_rays)
                }
            assert ray_tracing_param is not None

            start_time = time.time()
            for _ in range(n_trials):
                compute_room_irs(
                    room_dim=[8, 9, 3],
                    room_properties=0.5,  # rt60
                    scattering=0.5,
                    ism_order=ism_order
                    if _software == RoomSimSoftware.PYROOMACOUSTICS else None,
                    mic_pos=[0.3, 3, 0.2],
                    source_pos=[[3.2, 3, 1.8]],
                    software=_software,
                    ray_tracing_param=ray_tracing_param,
                )
            proc_time[ism_order][_software] = (time.time() - start_time) / float(n_trials)
            print("{} : {} seconds".format(_software, proc_time[ism_order][_software]))

    pprint.pprint(proc_time)

    # plot results
    plt.figure()
    for i, _software in enumerate(software):
        _proc_time = []
        for ism_order in ism_order_vals:
            if _software in proc_time[ism_order].keys():
                _proc_time.append(proc_time[ism_order][_software])
            else:
                break
        plt.plot(
            ism_order_vals[:len(_proc_time)],
            _proc_time,
            label=_software,
            marker=markers[i]
        )

    plt.legend()
    plt.xlabel("Specular depth / ISM order")
    plt.ylabel("Processing time [s]")
    plt.grid()
    plt.tight_layout()
    plt.savefig("ism.png")


if __name__ == "__main__":
    profile_room_gen()
