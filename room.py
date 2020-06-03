import glob
import json
import os
import shutil

from utils import get_subdirectories


class Room(object):
    def __init__(
        self,
        responses,
        mic_metadata,
        speaker_metadata,
        room_params,
        room_id,
        background_noise,
    ):

        self.id = room_id
        self.responses = responses
        self.n_mics = len(responses)
        self.n_speakers = len(responses[0])
        self.mic_metadata = mic_metadata
        self.speaker_metadata = speaker_metadata
        self.params = room_params
        self.background_noise = background_noise

    def save(self, destination_path):
        os.mkdir(destination_path)

        # -- room metadata
        config = {
            "id": self.id,
            "room_params": self.params,
            "speaker_metadata": self.speaker_metadata,
            "mic_metadata": self.mic_metadata,
        }
        metadata_path = os.path.join(destination_path, "config.json")
        with open(metadata_path, "w") as outfile:
            json.dump(config, outfile, indent=4, sort_keys=True)

        # -- room impulse responses
        rir_path = os.path.join(destination_path, "rir")
        os.mkdir(rir_path)
        for m, _mic in enumerate(self.responses):
            mic_path = os.path.join(rir_path, "mic{}".format(m))
            os.mkdir(mic_path)
            for n, _response in enumerate(_mic):
                shutil.copyfile(
                    _response, os.path.join(mic_path, "{}.wav".format(n))
                )

        # -- background noise
        background_noise_path = os.path.join(
            destination_path, "background_noise"
        )
        os.mkdir(background_noise_path)
        for k, _fp in enumerate(self.background_noise):
            shutil.copyfile(
                _fp, os.path.join(background_noise_path, "mic{}.wav".format(k))
            )

    @classmethod
    def load(cls, source_path):

        metadata_path = os.path.join(source_path, "config.json")
        rir_path = os.path.join(source_path, "rir")

        # load metadata
        with open(metadata_path) as json_file:
            metadata = json.load(json_file)

        # load responses
        mic_responses = get_subdirectories(rir_path)
        responses = []
        for _mic in mic_responses:
            rir_files = glob.glob(os.path.join(rir_path, _mic, "*.wav"))
            responses.append(rir_files)

        # load background if available
        background_noise_path = os.path.join(source_path, "background_noise")
        background_files = glob.glob(
            os.path.join(background_noise_path, "*.wav")
        )

        return cls(
            responses=responses,
            mic_metadata=metadata["mic_metadata"],
            speaker_metadata=metadata["speaker_metadata"],
            room_params=metadata["room_params"],
            room_id=metadata["id"],
            background_noise=background_files,
        )


class WallRegistry(object):
    WEST = "west"
    EAST = "east"
    NORTH = "north"
    SOUTH = "south"
    FLOOR = "floor"
    CEILING = "ceiling"
