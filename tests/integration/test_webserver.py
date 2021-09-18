# -*- coding: utf-8 -*-
"""
@author: Carlos Hernandez-Olivan
"""

# General modules
import json
import os
import pytest
import numpy as np
from pathlib import Path
import random

# Modules in this package
import webserver


@pytest.fixture(scope="module")
def test_config(tmp_path_factory):
    config = webserver.webserver_config.TestConfig
    # if config.BINARY_DIR is set in config file, don't override
    if config.BINARY_DIR is None:
        config.BINARY_DIR = tmp_path_factory.mktemp("checkpoints")
    yield config

@pytest.fixture
def client_conf_paths(test_config):
    app = webserver.create_app(
        config=test_config
    )

    yield app.test_client()

@pytest.fixture
def clients(client_conf_paths):
    yield [client_conf_paths]

def _assert_valid_response(
    response
):
    assert response.status_code == 201


def test_compose_musicvae(clients):
    post_data = {
        "command_name": "music_vae"
    }
    for client in clients:
        response = client.post("/api/command", json=post_data)
        _assert_valid_response(response)