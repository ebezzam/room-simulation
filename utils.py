import os
import numpy as np
import pyroomacoustics as pra
import pygsound as ps

from materials import materials_absorption_table


class RoomSimSoftware(object):
    PYROOMACOUSTICS = "pyroomacoustics"
    PYGSOUND = "pygsound"


def is_inside(source_loc, room_dim):
    """

    Determine if source is inside room and meets the minimum distance to wall
    constraint. Problem is very simplified as we assume ShoeBox room with
    walls aligned to x, y, and z axis.

    Parameters
    ------------
    source_loc : 3D array
        x, y, and z coordinates of source in question.
    room_dim : 3D array
        width, length, and height of room

    """
    for s, r in zip(*[source_loc, room_dim]):
        if s > r or s < 0:
            return False
    return True


def get_subdirectories(parent_dir):
    """
    Get immediate sub-directories of provided path.

    Return list of sub-directories.

    Parameters
    ----------
    parent_dir : str
        Path to directory whose sub-directories you wish to know.
    """
    return [
        name
        for name in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, name))
    ]


def rt60_to_absorption(room_dim, rt60):
    """
    Determine absorption factor given dimensions of (shoebox) room and RT60
    using Eyring's empirical equation.

    Parameters
    ------------
    room_dim : tuple / list
        Tuple / list of three elements, (width, length, height).
    rt60 : float
        Reverberation time (for 60 dB drop) in seconds.
    """
    width, length, height = room_dim
    vol = width * length * height
    area = 2 * (width * length + length * height + width * height)
    return 1.0 - np.exp(-0.163 * vol / rt60 / area)


def compute_room_irs(
    room_dim,
    mic_pos,
    source_pos,
    ray_tracing=False,
    room_properties=0.5,
    sample_rate=16000,
    ism_order=None,
    air_absorption=False,
    ray_tracing_param=None,
    scattering=0.5,
    temperature=None,
    software=RoomSimSoftware.PYROOMACOUSTICS,
):
    """

    Compute the RIRs between a provided mic position and one or multiple
    source position(s). Default is to apply Image Source Method (ISM) with
    order 17.

    Parameters
    ----------
    room_dim : array or list
        3D array, specifying (width, length, height) or a Shoebox room.
    mic_pos : array or list
        3D array specifying coordinates of microphone.
    source_pos : list of arrays
        List of coordinates for source positions.
    ray_tracing : bool
        Whether to apply ray tracing.
    room_properties : float or dict, optional
        If float, average RT60 of the room from which the average absorption is
        determined using Eyring's equation. If dict, one entry per wall in
        `WallRegistry` for the corresponding material.
    sample_rate : int, optional
        Sample rate in Hz.
    ism_order : int, optional
        Number of specular reflections to model with ISM.
    air_absorption : bool
        Whether to include air absorption in the simulation.
    ray_tracing_param : dict, optional
        Dict of parameters for ray tracing.
    scattering : float, optional
        Average scattering coefficient for all surfaces and frequencies.
    temperature : float, optional
        Temperature in Celsius.
    software : str, optional
        Which simulation software to use. "pyroomacoustics" (default) or
        "pygsound".
    """

    # check input parameters
    assert len(room_dim) == 3
    assert len(mic_pos) == 3
    mic_pos = np.array(mic_pos, ndmin=2).T
    for _pos in source_pos:
        assert len(_pos) == 3

    # prepare parameters
    energy_absorption = None
    scattering_config = {
        "description": "Flat scattering",
        "coeffs": [scattering],
    }
    if isinstance(room_properties, dict):
        materials_config = dict()
        for wall in room_properties:
            materials_config[wall] = pra.Material(
                energy_absorption=materials_absorption_table[
                    room_properties[wall]
                ],
                scattering=scattering_config,
            )
    elif isinstance(room_properties, float):
        energy_absorption = rt60_to_absorption(
            room_dim=room_dim, rt60=room_properties
        )
        materials_config = pra.Material(
            energy_absorption=energy_absorption, scattering=scattering_config
        )
    else:
        raise ValueError(
            "Invalid `materials`, must be `dict` with an entry"
            " for each wall or a `float` for an RT60."
        )

    # build room and simulate
    if software == RoomSimSoftware.PYROOMACOUSTICS:

        if ism_order is None:
            ism_order = 17

        pyroomacoustics_rt_param = {
            "n_rays": int(1e5),
            "receiver_radius": 0.5,
            "time_thres": 10.0,
        }
        if ray_tracing_param is not None:
            pyroomacoustics_rt_param.update(ray_tracing_param)

        room = pra.room.ShoeBox(
            p=room_dim,
            fs=sample_rate,
            materials=materials_config,
            max_order=ism_order,
            mics=pra.MicrophoneArray(mic_pos, sample_rate),
            air_absorption=air_absorption,
            ray_tracing=ray_tracing,
            temperature=temperature,
            humidity=0 if temperature is not None else None,
        )
        if ray_tracing:
            room.set_ray_tracing(**pyroomacoustics_rt_param)

        # add sources
        for _source_loc in source_pos:
            room.add_source(list(_source_loc))

        # compute RIRs
        room.compute_rir()
        rirs = room.rir[0]

    elif software == RoomSimSoftware.PYGSOUND:

        assert energy_absorption is not None
        assert isinstance(
            room_properties, float
        ), "`room_property` must be an RT60 value for `pygsound`"
        if air_absorption:
            print("Air absorption not available for `pygsound`.")
        if ism_order is not None:
            print("ISM order cannot be set for `pygsound`.")
        pygsound_param = {
            "diffuse_count": 20000,
            "specular_count": 2000,
            "src_radius": 0.01,
            "mic_radius": 0.01,
        }
        if ray_tracing_param is not None:
            pygsound_param.update(ray_tracing_param)

        # simulation variables
        ctx = ps.Context()
        ctx.diffuse_count = pygsound_param["diffuse_count"]
        ctx.specular_count = pygsound_param["specular_count"]
        if "specular_depth" in pygsound_param:
            ctx.specular_depth = pygsound_param["specular_depth"]
        ctx.channel_type = ps.ChannelLayoutType.mono
        ctx.sample_rate = sample_rate

        # create ShoeBox room
        mesh2 = ps.createbox(
            _width=room_dim[0],
            _length=room_dim[1],
            _height=room_dim[2],
            _absorp=energy_absorption,
            _scatter=scattering,
        )
        scene = ps.Scene()
        scene.setMesh(mesh2)

        # compute RIRs
        rirs = []
        for _pos in source_pos:
            _rir = pygsound_compute_ir(
                scene=scene,
                context=ctx,
                source_pos=_pos,
                mic_pos=mic_pos,
                src_radius=pygsound_param["src_radius"],
                mic_radius=pygsound_param["mic_radius"],
            )
            rirs.append(_rir)

    else:
        raise ValueError("Invalid simulation software.")

    return rirs, sample_rate


def pygsound_compute_ir(
    scene, context, source_pos, mic_pos, src_radius=0.01, mic_radius=0.01
):

    assert mic_pos.shape[0] == 3
    assert len(source_pos) == 3

    # set source and receiver
    src = ps.Source(source_pos)
    src.radius = src_radius
    lis = ps.Listener((mic_pos[:, 0]).tolist())
    lis.radius = mic_radius

    # compute IR
    res_ch = scene.computeIR(src, lis, context)
    ir = np.array(res_ch["samples"])
    if np.linalg.norm(ir) == 0.0:
        raise ValueError("Either source or mic is outside of room.")
    return ir
