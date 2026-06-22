import threading
import math
import logging
from typing import Dict, List, Tuple
from collections import deque

logger = logging.getLogger(__name__)

class EarlyStoppingGate:
    """
    Compute efficiency gate that monitors the performance of specific deck/policy branches.
    
    Maintains a rolling window of the global baseline win rate. If a specific branch
    performs significantly below this baseline (measured by Z-score), it is flagged for
    early termination to save compute cycles.
    """
    def __init__(self, baseline_window: int = 50, min_games: int = 5, z_threshold: float = 2.0):
        self.baseline_window = baseline_window
        self.min_games = min_games
        self.z_threshold = z_threshold
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Baseline history (global win/loss record 1.0 or 0.0)
        self.baseline_history: deque = deque(maxlen=baseline_window)
        
        # Track active branches: deck_hash -> list of results (1.0 or 0.0)
        self.active_branches: Dict[str, List[float]] = {}
        
        # Stats
        self.killed_branches = 0
        
    def record_result(self, deck_hash: str, won: bool):
        """Records a game result for a specific deck/policy branch."""
        val = 1.0 if won else 0.0
        with self.lock:
            # Update baseline
            self.baseline_history.append(val)
            
            # Update specific branch
            if deck_hash not in self.active_branches:
                self.active_branches[deck_hash] = []
            self.active_branches[deck_hash].append(val)

    def _get_baseline_stats(self) -> Tuple[float, float]:
        """Returns (mean, stddev) of baseline."""
        if not self.baseline_history:
            return 0.5, 0.5  # default
            
        mean = sum(self.baseline_history) / len(self.baseline_history)
        
        if len(self.baseline_history) < 2:
            return mean, 0.5
            
        variance = sum((x - mean) ** 2 for x in self.baseline_history) / (len(self.baseline_history) - 1)
        # Avoid 0 stddev
        stddev = max(0.01, math.sqrt(variance))
        return mean, stddev

    def should_stop(self, deck_hash: str) -> bool:
        """
        Returns True if the branch is performing significantly below baseline.
        """
        with self.lock:
            if deck_hash not in self.active_branches:
                return False
                
            results = self.active_branches[deck_hash]
            
            # Need minimum sample size to make a statistical judgment
            if len(results) < self.min_games:
                return False
                
            branch_mean = sum(results) / len(results)
            baseline_mean, baseline_std = self._get_baseline_stats()
            
            # Calculate Z-score
            z_score = (branch_mean - baseline_mean) / (baseline_std / math.sqrt(len(results)))
            
            # If z_score is very negative, it's performing worse than baseline
            if z_score < -self.z_threshold:
                self.killed_branches += 1
                logger.info(f"EarlyStoppingGate triggered for {deck_hash}: z={z_score:.2f} (branch_win={branch_mean:.2f}, baseline={baseline_mean:.2f})")
                return True
                
            return False

    def get_baseline_win_rate(self) -> float:
        with self.lock:
            mean, _ = self._get_baseline_stats()
            return mean

    def get_stats(self) -> dict:
        with self.lock:
            return {
                "baseline_samples": len(self.baseline_history),
                "baseline_win_rate": self.get_baseline_win_rate(),
                "active_branches": len(self.active_branches),
                "killed_branches": self.killed_branches
            }
