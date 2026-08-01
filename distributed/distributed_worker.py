"""
distributed/distributed_worker.py

A standalone rollout worker script designed to run on secondary CPU machines.
It fetches the latest network weights/archetype from Redis, simulates matches,
and streams serialized game trajectories back to a central Redis experience queue.
"""

import os
import sys
import time
import pickle
import logging

# Ensure correct path resolution
cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - Worker - %(levelname)s - %(message)s")
logger = logging.getLogger("DistributedWorker")

try:
    import redis
except ImportError:
    redis = None

from factory.game_runner import GameRunner, DEFAULT_DECK

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

from utils.load_latest_config import load_latest_config

from utils.main import main

if __name__ == "__main__":
    main()
