import json
import logging
from pathlib import Path

logger = logging.getLogger("orchestration_agent")


def get_training_scripts(enable_distributed: bool) -> list:
    if enable_distributed:
        logger.info("Distributed training mode ENABLED.")
        return [
            "distributed/master_server.py",
            "distributed/status_server.py",
            "scratch/run_ppo_trainer_loop.py",
            "scratch/run_deck_optimizer_loop.py",
        ]
    logger.info("Local training mode ENABLED.")
    return [
        "scratch/run_deck_optimizer_loop.py",
        "scratch/run_ppo_trainer_loop.py",
        "scratch/run_training_batches.py",
    ]


def read_fitness(path: str, key: str) -> float:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return float(data.get(key, -9999.0))
    except Exception:
        return -9999.0
