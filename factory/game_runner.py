"""
factory/game_runner.py

Executes exactly 3 games per iteration isolating variables using the actual CABT simulator:
1. Reasoning Test
2. Deck Test
3. Variance Baseline

Strictly enforces timeouts, checks win conditions, and generates iteration_result.json.
"""

import os
import time
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor

from agents.base_agent import BaseAgent
from factory.game_logger import GameLogger
from factory.game_agent_wrapper import CABTAgentWrapper

logger = logging.getLogger(__name__)

DEFAULT_DECK = [
    721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
    1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
    1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
    1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3
]

from factory.game_runner_worker import _parallel_game_worker

class GameRunner(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("GameRunner does not receive routed packets")

    def run_iteration(self, iteration_id: int, version_n1: str, version_n2: str, 
                       deck_base: Any, deck_new: Any, 
                       reasoning_base: dict, reasoning_new: dict) -> dict:
        d_base = deck_base.get("cards", DEFAULT_DECK) if isinstance(deck_base, dict) else deck_base
        d_new = deck_new.get("cards", DEFAULT_DECK) if isinstance(deck_new, dict) else deck_new
        if not isinstance(d_base, list): d_base = DEFAULT_DECK
        if not isinstance(d_new, list): d_new = DEFAULT_DECK

        games_config = [
            ("reasoning_test", d_base, d_base, False, True),
            ("deck_test", d_base, d_new, False, False),
            ("variance_baseline", d_base, d_base, False, False)
        ]

        results = {}
        num_workers = min(6, os.cpu_count() or 4)
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(_parallel_game_worker, str(self.log_dir), label, version_n1, version_n2, deck_a, deck_b, use_a, use_b)
                for label, deck_a, deck_b, use_a, use_b in games_config
            ]
            for future in futures:
                try:
                    res = future.result()
                    results[res["label"]] = res
                except Exception as e:
                    logger.error(f"Process execution crashed: {e}", exc_info=True)

        for label, _, _, _, _ in games_config:
            if label not in results:
                results[label] = {
                    "label": label, "winner": "error", "turns_taken": 0, "prizes_taken_a": 0,
                    "prizes_taken_b": 0, "time_elapsed": 0.0, "timeout": False,
                    "log_files": {"action": "", "reasoning": "", "variance": ""}
                }

        disk_results = {label: {k: v for k, v in res.items() if k != "steps_dump"} for label, res in results.items()}
        disk_payload = {
            "iteration": iteration_id, "timestamp": datetime.now().isoformat(),
            "games": disk_results, "ready_for_eval": True
        }
        (self.log_dir / "iteration_result.json").write_text(json.dumps(disk_payload, indent=2), encoding="utf-8")

        return {
            "iteration": iteration_id, "timestamp": datetime.now().isoformat(),
            "games": results, "ready_for_eval": True
        }

    def _run_single_game(self, label: str, v_a: str, v_b: str, 
                          deck_a: list[int], deck_b: list[int], use_staging_a: bool, use_staging_b: bool) -> dict:
        return _parallel_game_worker(str(self.log_dir), label, v_a, v_b, deck_a, deck_b, use_staging_a, use_staging_b)
