import socket
import threading
import time
import json
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from queue import Queue
from collections import deque
from distributed.work_order import WorkOrder, GameResult
from distributed.code_sync import get_local_version
from factory.game_runner import GameRunner
from distributed.master_handlers import MasterHandlers
from logging.handlers import RotatingFileHandler
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("master_server")
logger.setLevel(logging.INFO)
if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - Master - %(levelname)s - %(message)s')
    stream_h = logging.StreamHandler(sys.stdout)
    stream_h.setFormatter(formatter)
    logger.addHandler(stream_h)
    
    try:
        file_h = logging.FileHandler("logs/master_server.log", mode="a", encoding="utf-8")
        file_h.setFormatter(formatter)
        logger.addHandler(file_h)
    except Exception:
        pass

from ._load_deck import _load_deck
from .masterserver import MasterServer
from . import _setup
