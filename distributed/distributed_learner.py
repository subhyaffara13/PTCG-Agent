"""
distributed/distributed_learner.py

A standalone learner controller script designed to run on the main GPU node.
It pulls game experiences from Redis, batches them, performs policy updates,
and pushes updated weights back to Redis for worker processes to pull.
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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - Learner - %(levelname)s - %(message)s")
logger = logging.getLogger("DistributedLearner")

try:
    import redis
except ImportError:
    logger.error("redis-py is not installed. Please run: pip install redis")
    sys.exit(1)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

from utils.update_model_weights import update_model_weights

from utils.main import main

if __name__ == "__main__":
    main()
