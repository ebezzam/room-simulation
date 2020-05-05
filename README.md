# Room impulse response generation code

Supporting code for the paper "A study on more realistic room simulation for far-field keyword spotting".

RIR only dataset should be downloaded [here](https://speech.fit.vutbr.cz/software/but-speech-fit-reverb-database).

## Installation

First install Python dependencies:
```bash
pip install -r requirements.txt
```

Then install code for room impulse response generation:
```bash
# pyroomacoustics
pip install git+https://github.com/LCAV/pyroomacoustics.git@next_gen_simulator
# pygsound
pip install git+https://github.com/RoyJames/pygsound
```

For `pygsound`, please refer to their [project page](https://github.com/RoyJames/pygsound)
for additional dependencies to install.

## Scripts

Compare computation time between `pyroomacoustics` and `pygsound`: 
- Varying number of rays: `profile_nrays.py`
- Varying number of specular reflections / ISM order: `profile_ism_order.py`
