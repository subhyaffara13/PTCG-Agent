"""
factory/parallel_runner.py

Executes multiple game configurations concurrently using ProcessPoolExecutor.
"""

import os
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Any

from factory.parallel_runner_pool import (
    GameConfig,
    GameResult,
    _run_single_game,
)

logger = logging.getLogger(__name__)


class ParallelGameRunner:
    """
    Wraps GameRunner to execute multiple game configurations in parallel.
    """

    def __init__(self, max_workers: int = None, log_dir: str = "logs/parallel"):
        self.max_workers = max_workers or min(os.cpu_count() or 4, 6)
        self.log_dir = log_dir

    def _get_log_dir(self, config: GameConfig) -> str:
        suffix = f"iter_{config.iteration_id}_{config.label}" if config.label else f"iter_{config.iteration_id}"
        return os.path.join(self.log_dir, suffix)

    def run_all(self, configs: List[GameConfig]) -> List[GameResult]:
        """Runs game configs in parallel."""
        if not configs:
            return []

        results: List[GameResult] = []
        effective_workers = min(self.max_workers, len(configs))
        logger.info(f"Launching {len(configs)} games with {effective_workers} workers")

        with ProcessPoolExecutor(max_workers=effective_workers) as executor:
            future_to_config = {}
            for config in configs:
                game_log_dir = self._get_log_dir(config)
                future = executor.submit(_run_single_game, config, game_log_dir)
                future_to_config[future] = config

            for future in as_completed(future_to_config):
                config = future_to_config[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Game {config.label or config.iteration_id} completed successfully")
                except Exception as e:
                    logger.error(f"Game {config.label or config.iteration_id} raised: {e}", exc_info=True)
                    results.append(GameResult(config=config, result=None, success=False, error=str(e)))

        results.sort(key=lambda r: r.config.iteration_id)
        return results

    def run_all_sequential(self, configs: List[GameConfig]) -> List[GameResult]:
        """Runs configs sequentially (debugging)."""
        results = []
        for config in configs:
            result = _run_single_game(config, self._get_log_dir(config))
            results.append(result)
        results.sort(key=lambda r: r.config.iteration_id)
        return results

    def summarize(self, results: List[GameResult]) -> Dict[str, Any]:
        """Produces aggregate summary of all game results."""
        total = len(results)
        successes = sum(1 for r in results if r.success)
        win_counts = {"player_a": 0, "player_b": 0, "draw": 0, "error": 0}
        total_turns, games_with_turns = 0, 0

        for r in results:
            if not r.success or not r.result:
                win_counts["error"] += 1
                continue
            for game_data in r.result.get("games", {}).values():
                winner = game_data.get("winner", "error")
                win_counts[winner] = win_counts.get(winner, 0) + 1
                turns = game_data.get("turns_taken", 0)
                if turns > 0:
                    total_turns += turns
                    games_with_turns += 1

        avg = round(total_turns / games_with_turns, 1) if games_with_turns > 0 else 0
        return {
            "total_games": total,
            "successes": successes,
            "failures": total - successes,
            "win_distribution": win_counts,
            "avg_turns": avg,
        }
