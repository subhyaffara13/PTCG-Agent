from . import Any, Callable, Dict, Optional, Path, json, logger, math
from .optunamctstuner import OptunaMCTSTuner

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

        # Optuna tuner instance for MCTS hyperparameter tuning
        self.optuna_tuner = OptunaMCTSTuner()

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

    def get_mcts_params(self, iteration: Optional[int] = None, use_optuna: bool = False) -> Dict[str, Any]:
        """
        Get MCTS hyperparameters. If use_optuna is True, returns best Optuna tuned parameters.
        Otherwise calculates scheduled c_puct and default exploration/utility weights.
        """
        if use_optuna:
            return self.optuna_tuner.load_best_params()

        c_puct = self.get_c_puct(iteration) if iteration is not None else self.cpuct_start
        defaults = OptunaMCTSTuner.get_default_mcts_params()
        defaults["c_puct"] = c_puct
        return defaults

    def tune_mcts_with_optuna(self, eval_fn: Callable[[Dict[str, Any]], float], n_trials: int = 20) -> Dict[str, Any]:
        """Run Optuna tuning for MCTS parameters (c_puct, exploration rates, utility weights)."""
        return self.optuna_tuner.optimize(eval_fn, n_trials=n_trials)

    def get_all(self, iteration: int, use_optuna_mcts: bool = False) -> dict:
        """Return all hyperparameters for this iteration including MCTS params."""
        mcts_params = self.get_mcts_params(iteration, use_optuna=use_optuna_mcts)
        return {
            "learning_rate": self.get_learning_rate(iteration),
            "entropy_coef": self.get_entropy_coef(iteration),
            "c_puct": mcts_params["c_puct"],
            "mcts_exploration_rate": mcts_params.get("exploration_rate"),
            "mcts_utility_weights": mcts_params.get("utility_weights"),
            "clip_ratio": self.get_clip_ratio(iteration),
            "iteration": iteration,
            "progress": self._progress(iteration),
        }

    def save_state(self, iteration: int, use_optuna_mcts: bool = False):
        """Persist current state for crash recovery."""
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            state = self.get_all(iteration, use_optuna_mcts=use_optuna_mcts)
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

