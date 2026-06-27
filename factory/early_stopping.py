import threading
import logging
from typing import Dict, List
from collections import deque
from factory.early_stopping_helpers import calculate_baseline_stats, check_z_score_stop

logger = logging.getLogger(__name__)

class EarlyStoppingGate:
    """Compute efficiency gate that monitors branch performance."""
    def __init__(self, baseline_window: int = 50, min_games: int = 5, z_threshold: float = 2.0):
        self.baseline_window = baseline_window
        self.min_games = min_games
        self.z_threshold = z_threshold
        
        self.lock = threading.Lock()
        self.baseline_history = deque(maxlen=baseline_window)
        self.active_branches: Dict[str, List[float]] = {}
        self.killed_branches = 0
        
    def record_result(self, deck_hash: str, won: bool):
        val = 1.0 if won else 0.0
        with self.lock:
            self.baseline_history.append(val)
            if deck_hash not in self.active_branches:
                self.active_branches[deck_hash] = []
            self.active_branches[deck_hash].append(val)

    def should_stop(self, deck_hash: str) -> bool:
        with self.lock:
            if deck_hash not in self.active_branches:
                return False
            results = self.active_branches[deck_hash]
            stop, z, b_mean, bl_mean = check_z_score_stop(
                results, list(self.baseline_history), self.min_games, self.z_threshold
            )
            if stop:
                self.killed_branches += 1
                logger.info(f"EarlyStoppingGate triggered for {deck_hash}: z={z:.2f} (branch_win={b_mean:.2f}, baseline={bl_mean:.2f})")
                return True
            return False

    def get_baseline_win_rate(self) -> float:
        with self.lock:
            mean, _ = calculate_baseline_stats(list(self.baseline_history))
            return mean

    def get_stats(self) -> dict:
        with self.lock:
            return {
                "baseline_samples": len(self.baseline_history),
                "baseline_win_rate": self.get_baseline_win_rate(),
                "active_branches": len(self.active_branches),
                "killed_branches": self.killed_branches
            }
