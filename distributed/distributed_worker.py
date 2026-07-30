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

def load_latest_config(r):
    """Fetch the latest archetype and model weights from Redis or local cache."""
    if not r:
        return "aggro", None
    try:
        archetype = r.get("ptcg:latest_archetype")
        archetype = archetype.decode("utf-8") if archetype else "aggro"
        weights_bytes = r.get("ptcg:latest_weights")
        weights = pickle.loads(weights_bytes) if weights_bytes else None  # nosec B301
        return archetype, weights
    except Exception as e:
        logger.warning(f"Failed to load configuration from Redis: {e}")
        return "aggro", None

def main():
    os.environ["IS_WORKER"] = "true"
    r = None
    if redis is not None:
        try:
            client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, socket_timeout=2)
            client.ping()
            r = client
            logger.info(f"Connected to central Redis at {REDIS_HOST}:{REDIS_PORT}")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}). Operating in local multi-process self-play worker mode.")
    
    runner = GameRunner()
    
    logger.info("Rollout worker started. Beginning loop...")
    while True:
        # 1. Fetch latest policy configuration/weights from central node
        archetype, weights = load_latest_config(r)
        
        # 2. Run simulation
        logger.info(f"Running simulation with archetype: {archetype}")
        try:
            # Simulate a match
            iteration_result = runner.run_iteration(
                iteration_id=0,
                version_n1="base_v0",
                version_n2="new_v0",
                deck_base=DEFAULT_DECK,
                deck_new=DEFAULT_DECK,
                reasoning_base={},
                reasoning_new={}
            )
            
            # 3. Serialize and push rollout trajectories to central queue
            if r:
                payload = pickle.dumps({
                    "archetype": archetype,
                    "result": iteration_result,
                    "timestamp": time.time()
                })
                r.rpush("ptcg:experience_queue", payload)
                logger.info("Successfully pushed rollout trajectory to experience queue.")
            else:
                logger.info("Simulation completed cleanly in local worker mode.")
            
        except Exception as e:
            logger.error(f"Error during simulation run: {e}", exc_info=True)
            time.sleep(5)  # Backoff on error

if __name__ == "__main__":
    main()
