# -*- coding: utf-8 -*-
"""
@author: Carlos
"""

import logging
from pathlib import Path


class Config:
    """Base config vars."""

    pass


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SESSION_TYPE = "filesystem"
    LOGGING_FILENAME = None
    LOGGING_LEVEL = None
    INTERNAL_SERVER_ERROR_STACKTRACE = True
    BINARY_DIR = Path("checkpoints")


class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SESSION_TYPE = "filesystem"
    LOGGING_FILENAME = "tmp/dev/log.txt"
    LOGGING_LEVEL = logging.DEBUG
    INTERNAL_SERVER_ERROR_STACKTRACE = True
    BINARY_DIR = Path("checkpoints")


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_TYPE = "redis"
    LOGGING_FILENAME = "log.txt"
    LOGGING_LEVEL = logging.INFO
    INTERNAL_SERVER_ERROR_STACKTRACE = False
    BINARY_DIR = Path("checkpoints")