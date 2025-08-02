# dist/ba_root/mods/__init__.py
"""Custom hooks to pull of the in-game functions."""

# ba_meta require api 9
# (see https://ballistica.net/wiki/meta-tag-system)

# pylint: disable=import-error
# pylint: disable=import-outside-toplevel
# pylint: disable=protected-access

from __future__ import annotations

import _thread
import importlib
import logging
import os
import time
from datetime import datetime
from typing import TYPE_CHECKING

import babase

import bomb

if TYPE_CHECKING:
    from typing import Any

import utils
import logger

# ba_meta export babase.Plugin
class modSetup(babase.Plugin):
    def on_app_running(self):
        bomb.apply_bomb_mods()
        logger.log_success("BombSquad Mods initialized successfully!")

    def on_app_shutdown(self):
        logger.log_warning("All BombSquad Mods shutting down...")        