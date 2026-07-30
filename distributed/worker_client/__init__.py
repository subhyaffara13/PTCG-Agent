import sys
import os
import subprocess
import time
import io
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)
import contextlib
import socket
import logging
import uuid
from distributed.work_order import WorkOrder, GameResult
from factory.game_runner import GameRunner
logging.basicConfig(level=logging.INFO, format='%(asctime)s - Worker - %(levelname)s - %(message)s')
logger = logging.getLogger("worker_client")
_MAX_RETRIES = 15
_CONNECT_TIMEOUT = 5.0  # Short timeout for initial TCP connect
_READ_TIMEOUT = 120.0    # Longer timeout for MCTS runs (per-read)
_STARTUP_WATCHDOG = 300  # 5 minutes: if we can't get a complete cycle, bail

from .dummystream_silence_kaggle_warnings import DummyStream
from .dummystream_silence_kaggle_warnings import silence_kaggle_warnings
from .ensure_dependencies import ensure_dependencies
from ._backoff_sleep import _backoff_sleep
from .workerclient import WorkerClient
from . import _setup
