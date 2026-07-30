"""
factory/game_runner.py
Runs parallel game playouts for iteration evaluations.
"""
import os
import time
import json
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from cb_agents.base_agent import BaseAgent
from factory.game_runner_worker import _parallel_game_worker
logger = logging.getLogger(__name__)

from ._mutate_deck__load_optimized_deck import _mutate_deck
from ._mutate_deck__load_optimized_deck import _load_optimized_deck
from .gamerunner import GameRunner
from ._setup import DEFAULT_DECK
