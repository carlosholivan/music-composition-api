# general modules
from typing import List
import os
from six.moves import urllib

# tf module
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# magenta modules
from magenta.models.music_vae import TrainedModel, configs
from note_seq.protobuf.music_pb2 import NoteSequence

def download_checkpoint(model_name: str,
                        checkpoint_name: str,
                        target_dir: str):
    """
    Downloads a Magenta checkpoint to target directory.

    Target directory target_dir will be created if it does not already exist.

        :param model_name: magenta model name to download
        :param checkpoint_name: magenta checkpoint name to download
        :param target_dir: local directory in which to write the checkpoint
    """
    tf.gfile.MakeDirs(target_dir)
    checkpoint_target = os.path.join(target_dir, checkpoint_name)
    if not os.path.exists(checkpoint_target):
        response = urllib.request.urlopen(
            f"https://storage.googleapis.com/magentadata/models/"
            f"{model_name}/checkpoints/{checkpoint_name}")
        data = response.read()
        local_file = open(checkpoint_target, 'wb')
        local_file.write(data)
        local_file.close()

def get_model(name: str):
    """
    Returns the model instance from its name.

        :param name: the model name
    """
    checkpoint = name + ".tar"
    #download_checkpoint("music_vae", checkpoint, "checkpoints")
    return TrainedModel(
        # Removes the .lohl in some training checkpoint which shares the same config
        configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
        # The batch size changes the number of sequences to be processed together,
        # we'll be working with maximum 6 sequences (during groove)
        batch_size=8,
        checkpoint_dir_or_path=os.path.join("checkpoints", checkpoint))

def sample(model_name: str,
           num_steps_per_sample: int) -> List[NoteSequence]:
    """
    Samples 2 sequences using the given model.
    """
    model = get_model(model_name)

    # Uses the model to sample 2 sequences,
    # with the number of steps and default temperature
    sample_sequences = model.sample(n=2, length=num_steps_per_sample, 
                                    temperature=1.1)

    # Saves the midi and the plot in the sample folder
    #save_midi(sample_sequences, "sample", model_name)
    #save_plot(sample_sequences, "sample", model_name)

    return sample_sequences