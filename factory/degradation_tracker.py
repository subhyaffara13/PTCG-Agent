import json
import logging
import math
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class DegradationReport:
    """
    Represents the output of a system health evaluation.
    
    Attributes:
        is_degraded: True if the system is suffering from policy collapse or win-rate drops.
        health_score: 0.0 to 1.0 (1.0 being perfectly healthy).
        reasons: List of strings explaining why the system is degraded.
        suggested_action: Command string for the orchestrator (e.g., 'trigger_deck_optimizer').
    """
    is_degraded: bool
    health_score: float
    reasons: List[str]
    suggested_action: str

class DegradationTracker:
    """
    Monitors long-term agent health to prevent catastrophic forgetting and policy collapse.
    
    This module tracks baseline win-rates and behavioral diversity over a rolling window.
    If performance drops below critical thresholds, it acts as an emergency stop, capable of
    pausing the training loop and generating a DegradationReport to trigger optimizer subagents.
    It also extracts 'do's' (healthy patterns) from overwhelmingly successful iterations.
    """
    def __init__(self, history_window: int = 100, skills_dir: str = "skills"):
        self.history_window = history_window
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.learned_dos_file = self.skills_dir / "learned_dos.json"
        self.learned_dos = self._load_dos()
        
        # In-memory history tracking
        self.win_rate_history: List[float] = []
        self.diversity_history: List[float] = []
        
    def _load_dos(self) -> Dict[str, List[Any]]:
        if self.learned_dos_file.exists():
            try:
                return json.loads(self.learned_dos_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return {"deck_dos": [], "behavior_dos": []}

    def _save_dos(self):
        try:
            self.learned_dos_file.write_text(json.dumps(self.learned_dos, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to save learned dos: {e}")

    def record_iteration_stats(self, win_rate: float, diversity_score: float):
        """Called at the end of every iteration or batch of iterations."""
        self.win_rate_history.append(win_rate)
        self.diversity_history.append(diversity_score)
        
        # Keep within window
        if len(self.win_rate_history) > self.history_window:
            self.win_rate_history.pop(0)
            self.diversity_history.pop(0)

    def evaluate_health(self) -> DegradationReport:
        """
        Evaluates system health based on the tracked history.
        Returns a DegradationReport.
        """
        if len(self.win_rate_history) < 10:
            # Not enough data to judge degradation
            return DegradationReport(False, 1.0, [], "continue")
            
        # Calculate trends (comparing first half of window to second half)
        mid = len(self.win_rate_history) // 2
        old_wr = sum(self.win_rate_history[:mid]) / max(1, mid)
        new_wr = sum(self.win_rate_history[mid:]) / max(1, len(self.win_rate_history) - mid)
        
        old_div = sum(self.diversity_history[:mid]) / max(1, mid)
        new_div = sum(self.diversity_history[mid:]) / max(1, len(self.diversity_history) - mid)
        
        reasons = []
        is_degraded = False
        action = "continue"
        
        # Health Score: 1.0 is stable/improving. < 0.5 is degraded.
        health_score = 1.0
        
        if new_wr < old_wr * 0.7:  # 30% drop in win rate
            reasons.append(f"Catastrophic win rate collapse: {old_wr:.2f} -> {new_wr:.2f}")
            health_score -= 0.6
            is_degraded = True
            
        if new_div < 0.05 and old_div > 0.1:  # Diversity collapse (policy collapse)
            reasons.append("Policy mode collapse (diversity dropped near 0).")
            health_score -= 0.4
            is_degraded = True
            
        if is_degraded:
            if "win rate" in "".join(reasons).lower():
                action = "trigger_deck_optimizer"
            else:
                action = "trigger_strategy_optimizer"
                
        return DegradationReport(
            is_degraded=is_degraded,
            health_score=max(0.0, health_score),
            reasons=reasons,
            suggested_action=action
        )

    def extract_healthy_patterns(self, iteration_result: Dict[str, Any], behavioral_vectors: Dict[str, Any], decks: Dict[str, list]):
        """
        If the iteration was extremely successful, extract 'Dos'.
        """
        for label, game in iteration_result.get("games", {}).items():
            if game.get("winner") == "player_b":  # Assume player_b is our agent
                prizes_taken_b = game.get("prizes_taken_b", 0)
                turns = game.get("turns_taken", 999)
                
                # Overwhelming victory heuristic
                if prizes_taken_b == 6 and turns < 12:
                    logger.info("DegradationTracker: Extracting healthy pattern from overwhelming victory.")
                    bv_b = behavioral_vectors.get("player_b")
                    if bv_b and bv_b.energy_accel_rate > 1.0:
                        rule = {"condition": "high_accel_wins", "description": "Energy accel > 1.0 strongly correlates with fast wins."}
                        if rule not in self.learned_dos["behavior_dos"]:
                            self.learned_dos["behavior_dos"].append(rule)
                            self._save_dos()
