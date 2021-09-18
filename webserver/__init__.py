# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 09:18:47 2021

@author: Carlos
"""

# General modules
import traceback
import os
from pathlib import Path
import sys
from typing import Optional
import shutil
import json 
import weakref
import tempfile

# Flask modules
from flask import Flask, jsonify, request, safe_join, send_file
from flask.logging import create_logger
from flask_cors import cross_origin

# Modules in this package
from magenta.music import DEFAULT_STEPS_PER_BAR
import note_seq
from models.musicvae import sample
from webserver.webserver_config import Config, DevConfig


class FileRemover(object):
    def __init__(self):
        self.weak_references = dict()  # weak_ref -> filepath to remove

    def cleanup_once_done(self, response, filepath):
        wr = weakref.ref(response, self._do_cleanup)
        self.weak_references[wr] = filepath

    def _do_cleanup(self, wr):
        filepath = self.weak_references[wr]
        print('Deleting %s' % filepath)
        shutil.rmtree(filepath, ignore_errors=True)

file_remover = FileRemover()

def create_app(
    config: Config = DevConfig
):
    """
    Creates the app from a config.
    """

    # Create and configure an instance of the Flask application.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    log = create_logger(app)

    # Configure logging.
    # logging_filename = app.config["LOGGING_FILENAME"]
    logging_level = app.config["LOGGING_LEVEL"]
    if logging_level is not None:
        app.logger.setLevel(logging_level)

    # Start app
    app.logger.info("Starting app...")

    @app.route("/api/command", methods=["POST"])
    @cross_origin()
    def compose():
        """
        Accepts a command sent via POST. Processed the command and returns a result.
        """

        try:

            params = request.get_json()

            log.info("Got params {}".format(params))

            # Check if the command comes as its name and with some parameters.
            valid_command_names = ["music_vae", "music_transformer"]

            errors = []
            if "command_name" not in params:
                errors += ["Missing command_name."]
            if (
                "command_name" in params
                and params["command_name"] not in valid_command_names
            ):
                errors += [
                    f"Unexpected command. Expected one of {valid_command_names}."
                ]

            if len(errors) != 0:
                return jsonify({"errors": errors}), 400

            # Parse the command.
            command_name = params["command_name"]

            # compose means that the API returns a full composition from scratch
            if command_name == "music_vae":

                # Cretate temporary directory  to save json and midi 
                temp_path = tempfile.mkdtemp()

                # Number of interpolated sequences (counting the start and end sequences)
                num_output = 6

                # Number of bar per sample, also giving the size of the interpolation splits
                num_bar_per_sample = 4

                # Number of steps per sample and interpolation splits
                num_steps_per_sample = num_bar_per_sample * DEFAULT_STEPS_PER_BAR

                # The total number of bars
                total_bars = num_output * num_bar_per_sample

                # Samples new sequences with "lokl" model which is optimized for sampling
                generated_sample_sequences = sample("cat-drums_2bar_small.lokl",
                                                    num_steps_per_sample)

                # Save MIDI file in a temp directory
                midi_filename = 'midi_filename.mid'
                #log.info("Creating MIDI file {} from {}...".format(midi_filename, temp_path))
                midi_path = safe_join(temp_path, midi_filename)
                note_seq.sequence_proto_to_midi_file(generated_sample_sequences[0], midi_path)
                #log.info('Saved MIDI file in {}'.format(midi_path))
            
                resp = send_file(midi_path,
                                mimetype='audio/midi',
                                )

                # Delete temporary directory            
                file_remover.cleanup_once_done(resp, temp_path)
                return resp, 201

        except Exception as e:
            app.logger.error(e)
            traceback.print_exc(file=sys.stdout)

            if app.config["INTERNAL_SERVER_ERROR_STACKTRACE"]:
                response_string = str() + " - " + str(traceback.format_exc())
                app.logger.error(response_string)
            else:
                response_string = "Internal Server Error."

            return jsonify({"error": response_string}), 500

    return app