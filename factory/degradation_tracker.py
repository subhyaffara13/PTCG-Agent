import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path
from factory.degradation_helpers import evaluate_degradation_health, extract_healthy_behavior_patterns

logger = logging.getLogger(__name__)

@dataclass
class DegradationReport:
    is_degraded: bool
    health_score: float
    reasons: List[str]
    suggested_action: str

class DegradationTracker:
    """Monitors long-term agent health to prevent policy collapse."""
    def __init__(self, history_window: int = 100, skills_dir: str = "skills"):
        self.history_window = history_window
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.learned_dos_file = self.skills_dir / "learned_dos.json"
        self.learned_dos = self._load_dos()
        
        self.win_rate_history: List[float] = []
        self.diversity_history: List[float] = []
        
    def _load_dos(self) -> Dict[str, List[Any]]:
        if self.learned_dos_file.exists():
            try: return json.loads(self.learned_dos_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError: pass
        return {"deck_dos": [], "behavior_dos": []}

    def _save_dos(self):
        try: self.learned_dos_file.write_text(json.dumps(self.learned_dos, indent=2), encoding="utf-8")
        except Exception as e: logger.error(f"Failed to save learned dos: {e}")

    def record_iteration_stats(self, win_rate: float, diversity_score: float):
        """Called at the end of every iteration or batch."""
        self.win_rate_history.append(win_rate)
        self.diversity_history.append(diversity_score)
        
        if len(self.win_rate_history) > self.history_window:
            self.win_rate_history.pop(0)
            self.diversity_history.pop(0)

    def evaluate_health(self) -> DegradationReport:
        res = evaluate_degradation_health(self.win_rate_history, self.diversity_history)
        return DegradationReport(
            is_degraded=res["is_degraded"],
            health_score=res["health_score"],
            reasons=res["reasons"],
            suggested_action=res["suggested_action"]
        )

    def extract_healthy_patterns(self, iteration_result: Dict[str, Any], behavioral_vectors: Dict[str, Any], decks: Dict[str, list]):
        extract_healthy_behavior_patterns(iteration_result, behavioral_vectors, self.learned_dos, self._save_dos)
