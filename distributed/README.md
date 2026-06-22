# Decoupled Distributed Training Pipeline (Redis / ZeroMQ)

This folder contains a prototype setup for distributing Pokémon TCG rollout simulations and neural network optimization across multiple nodes using Redis as an asynchronous queue and parameter store.

## Architecture Layout

```
                        +----------------------------+
                        |  CPU Workers (Self-Play)   |
                        |  - distributed_worker.py   |
                        +--------------+-------------+
                                       |
                   Pushes rollouts     |      Pulls latest policy
                   to queue            |      weights/archetypes
                                       v
                        +--------------+-------------+
                        |  Central Redis Database    |
                        |  - Queue: ptcg:experience   |
                        |  - Store: ptcg:weights      |
                        +--------------+-------------+
                                       |
                   Batches experiences |      Saves optimized
                   from Redis          |      policy weights
                                       v
                        +--------------+-------------+
                        |  GPU Learner (Optimizer)   |
                        |  - distributed_learner.py  |
                        +----------------------------+
```

## Setup Instructions

### 1. Install Redis
On the central node (or GPU learner host), install and run Redis:
* **Ubuntu/Debian:** `sudo apt-get install redis-server`
* **Windows/macOS:** Use Docker: `docker run -d -p 6379:6379 redis`

### 2. Configure Network/Firewall Access
By default, Redis binds to `127.0.0.1`. If workers are on different computers, edit `/etc/redis/redis.conf`:
```conf
bind 0.0.0.0
protected-mode no
```
*Restart Redis:* `sudo systemctl restart redis-server`

Ensure port `6379` is open in the firewall on the host machine to allow external workers to connect.

### 3. Run the Learner
On your main GPU training machine:
```bash
export REDIS_HOST="localhost"
python distributed/distributed_learner.py
```

### 4. Run the Workers
On any other secondary CPU-heavy computers:
```bash
export REDIS_HOST="<IP_OF_GPU_LEARNER>"
python distributed/distributed_worker.py
```

---

## Technical Advantages

1. **Failure Tolerance**: If a worker node crashes or loses network connectivity, the training does not halt. Stale or incomplete rollouts simply drop out of the pipeline, and active workers continue streaming.
2. **Dynamic Scaling**: Workers can be added or removed on the fly by starting or stopping python processes on auxiliary laptops or desktops.
3. **No Lock-Step Stalling**: The learner pulls batches and computes gradient steps asynchronously without needing to wait for any single worker to finish.
