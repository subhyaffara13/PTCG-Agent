"""
factory/game_runner.py
Runs parallel game playouts for iteration evaluations.
"""
import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from agents.base_agent import BaseAgent
from factory.game_runner_worker import _parallel_game_worker

logger = logging.getLogger(__name__)

DEFAULT_DECK = [
    721, 721, 722, 722, 722, 722, 723, 723, 723, 723,
    1092, 1121, 1121, 1145, 1145, 1163, 1163, 1219,
    1219, 1219, 1219, 1227, 1227, 1227, 1227, 1262,
    1262, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3
]

class GameRunner(BaseAgent):
    _executor = None

    def __init__(self, log_dir: str = "logs", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        if GameRunner._executor is None:
            GameRunner._executor = ProcessPoolExecutor(max_workers=os.cpu_count() or 16)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError("GameRunner does not receive routed packets")

    def run_iteration(self, iteration_id: int, version_n1: str, version_n2: str, 
                       deck_base: Any, deck_new: Any, 
                       reasoning_base: dict, reasoning_new: dict) -> dict:
        d_base = deck_base.get("cards", DEFAULT_DECK) if isinstance(deck_base, dict) else deck_base
        d_new = deck_new.get("cards", DEFAULT_DECK) if isinstance(deck_new, dict) else deck_new
        if not isinstance(d_base, list): d_base = DEFAULT_DECK
        if not isinstance(d_new, list): d_new = DEFAULT_DECK

        # RUN 100 PLAYS IN PARALLEL: 50 deck tests and 50 variance tests
        games_config = [("reasoning_test", d_base, d_base, False, True)]
        for j in range(50):
            games_config.extend([
                (f"deck_test_{j}", d_base, d_new, False, False),
                (f"variance_baseline_{j}", d_base, d_base, False, False)
            ])

        results = {}
        futures = [
            GameRunner._executor.submit(_parallel_game_worker, str(self.log_dir), label, version_n1, version_n2, deck_a, deck_b, use_a, use_b)
            for label, deck_a, deck_b, use_a, use_b in games_config
        ]
        for future in futures:
            try:
                res = future.result()
                results[res["label"]] = res
            except Exception as e:
                logger.error(f"Process execution crashed: {e}", exc_info=True)

        # Consolidate results for EvalAgent (average metrics across 5 parallel runs)
        for prefix, key in [("deck_test", "deck_test"), ("variance_baseline", "variance_baseline")]:
            workers = [res for k, res in results.items() if k.startswith(prefix)]
            if workers:
                win_counts = Counter(w.get("winner") for w in workers)
                results[key] = {
                    "label": key, "winner": win_counts.most_common(1)[0][0],
                    "turns_taken": int(sum(w.get("turns_taken", 0) for w in workers) / len(workers)),
                    "prizes_taken_a": int(sum(w.get("prizes_taken_a", 0) for w in workers) / len(workers)),
                    "prizes_taken_b": int(sum(w.get("prizes_taken_b", 0) for w in workers) / len(workers)),
                    "time_elapsed": workers[0].get("time_elapsed", 0.0),
                    "timeout": any(w.get("timeout") for w in workers),
                    "log_files": workers[0].get("log_files", {})
                }

        # Ensure fallback keys
        for k in ["reasoning_test", "deck_test", "variance_baseline"]:
            if k not in results:
                results[k] = {"winner": "error", "turns_taken": 0, "log_files": {}}

        disk_results = {label: {k: v for k, v in res.items() if k != "steps_dump"} for label, res in results.items()}
        disk_payload = {
            "iteration": iteration_id, "timestamp": datetime.now().isoformat(),
            "games": disk_results, "ready_for_eval": True
        }
        (self.log_dir / "iteration_result.json").write_text(json.dumps(disk_payload, indent=2), encoding="utf-8")

        return {"iteration": iteration_id, "timestamp": datetime.now().isoformat(), "games": results, "ready_for_eval": True}
