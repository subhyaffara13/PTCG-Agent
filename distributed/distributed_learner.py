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

def update_model_weights(model, batch_experiences):
    """
    Dummy optimizer update function. In a real setup, this would format
    batch_experiences into PyTorch tensors and run model optimizer step.
    """
    logger.info(f"Optimizing policy network using batch of {len(batch_experiences)} game rollouts...")
    # Simulate forward/backward pass processing time
    time.sleep(0.5)
    
    # Return simulated weights
    return {"dummy_weights": [0.1, 0.2, 0.3]}

def main():
    logger.info(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    
    # Clear any stale queues on start
    # r.delete("ptcg:experience_queue")
    
    # Store initial model weights
    initial_weights = {"dummy_weights": [0.0, 0.0, 0.0]}
    r.set("ptcg:latest_weights", pickle.dumps(initial_weights))
    r.set("ptcg:latest_archetype", "aggro")
    
    batch_size = 5
    batch_experiences = []
    
    logger.info("Learner initialized. Awaiting experiences from workers...")
    while True:
        # Block until an experience is pushed to the queue
        _, payload = r.blpop("ptcg:experience_queue")
        
        try:
            experience = pickle.loads(payload)  # nosec B301
            batch_experiences.append(experience)
            logger.info(f"Received experience payload. Batch progress: {len(batch_experiences)}/{batch_size}")
            
            if len(batch_experiences) >= batch_size:
                # Run Optimization update step
                new_weights = update_model_weights(None, batch_experiences)
                
                # Push the updated weights back to Redis
                r.set("ptcg:latest_weights", pickle.dumps(new_weights))
                logger.info("Updated weights pushed to Redis.")
                
                # Clear batch
                batch_experiences = []
                
        except Exception as e:
            logger.error(f"Error processing experience payload: {e}", exc_info=True)

if __name__ == "__main__":
    main()
