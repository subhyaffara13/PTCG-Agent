"""
factory/hyperparam_scheduler.py

Dynamic hyperparameter annealing for PPO training.
Supports cosine, linear, and step decay schedules.
"""
import json
import math
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class HyperparamScheduler:
    def __init__(self, total_iterations: int = 500):
        self.total_iterations = max(1, total_iterations)
        self.state_path = Path("models/hyperparam_state.json")

        # Learning rate: cosine annealing
        self.lr_start = 1e-3
        self.lr_end = 1e-5

        # Entropy coefficient: linear decay
        self.entropy_start = 0.08
        self.entropy_end = 0.01

        # C_puct: step decay
        self.cpuct_start = 1.25
        self.cpuct_end = 0.8
        self.cpuct_step_interval = 50

        # Clip ratio: linear decay
        self.clip_start = 0.2
        self.clip_end = 0.1

    def _progress(self, iteration: int) -> float:
        """Return progress ratio [0.0, 1.0]."""
        return min(1.0, max(0.0, iteration / self.total_iterations))

    def get_learning_rate(self, iteration: int) -> float:
        """Cosine annealing: lr_start -> lr_end."""
        progress = self._progress(iteration)
        cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
        return self.lr_end + (self.lr_start - self.lr_end) * cosine_decay

    def get_entropy_coef(self, iteration: int) -> float:
        """Linear decay: entropy_start -> entropy_end."""
        progress = self._progress(iteration)
        return self.entropy_start + (self.entropy_end - self.entropy_start) * progress

    def get_c_puct(self, iteration: int) -> float:
        """Step decay: drop by fixed amount every cpuct_step_interval iterations."""
        num_steps = iteration // self.cpuct_step_interval
        total_steps = self.total_iterations // self.cpuct_step_interval
        if total_steps <= 0:
            return self.cpuct_start
        step_size = (self.cpuct_start - self.cpuct_end) / total_steps
        value = self.cpuct_start - num_steps * step_size
        return max(self.cpuct_end, value)

    def get_clip_ratio(self, iteration: int) -> float:
        """Linear decay: clip_start -> clip_end."""
        progress = self._progress(iteration)
        return self.clip_start + (self.clip_end - self.clip_start) * progress

    def get_all(self, iteration: int) -> dict:
        """Return all hyperparameters for this iteration."""
        return {
            "learning_rate": self.get_learning_rate(iteration),
            "entropy_coef": self.get_entropy_coef(iteration),
            "c_puct": self.get_c_puct(iteration),
            "clip_ratio": self.get_clip_ratio(iteration),
            "iteration": iteration,
            "progress": self._progress(iteration),
        }

    def save_state(self, iteration: int):
        """Persist current state for crash recovery."""
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            state = self.get_all(iteration)
            self.state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to save hyperparam state: {e}")

    @staticmethod
    def load_state() -> dict:
        """Load persisted state. Returns empty dict if not found."""
        path = Path("models/hyperparam_state.json")
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}
