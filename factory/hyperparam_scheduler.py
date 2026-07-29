"""
factory/hyperparam_scheduler.py

Dynamic hyperparameter annealing for PPO training and Optuna-based
hyperparameter tuning for MCTS parameters (c_puct, exploration rates, utility weights).
"""
import json
import math
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable

logger = logging.getLogger(__name__)

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    optuna = None
    OPTUNA_AVAILABLE = False


class OptunaMCTSTuner:
    """
    Optuna-based hyperparameter optimization tuner for MCTS parameters:
    - c_puct (UCB exploration constant)
    - Exploration rates (dirichlet_alpha, dirichlet_epsilon, temperature)
    - Utility weights (prize_weight, hp_weight, energy_weight, bench_weight, win_weight)
    """

    def __init__(self, study_name: str = "mcts_hyperparam_tuning", storage: Optional[str] = None):
        if not OPTUNA_AVAILABLE:
            logger.warning("Optuna is not installed. OptunaMCTSTuner functions will run in fallback mode.")
        self.study_name = study_name
        self.storage = storage
        self.best_params_path = Path("models/optuna_mcts_best.json")

    @staticmethod
    def sample_mcts_params(trial: Any) -> Dict[str, Any]:
        """
        Sample MCTS parameters from an Optuna trial.

        Parameters tuned:
        - c_puct: UCB exploration coefficient [0.5, 3.0]
        - exploration rates:
            - dirichlet_alpha: Dirichlet noise alpha [0.01, 0.5]
            - dirichlet_epsilon: Dirichlet noise mix ratio [0.0, 0.5]
            - temperature: Policy search temperature [0.1, 1.5]
        - utility weights:
            - prize_weight: Weight for prize card advantage [0.5, 5.0]
            - hp_weight: Weight for HP differential [0.1, 2.0]
            - energy_weight: Weight for attached energy [0.1, 2.0]
            - bench_weight: Weight for bench presence [0.1, 2.0]
            - win_weight: Weight for terminal win state [10.0, 100.0]
        """
        if not OPTUNA_AVAILABLE or trial is None:
            return OptunaMCTSTuner.get_default_mcts_params()

        c_puct = trial.suggest_float("c_puct", 0.5, 3.0)
        dirichlet_alpha = trial.suggest_float("dirichlet_alpha", 0.01, 0.5)
        dirichlet_epsilon = trial.suggest_float("dirichlet_epsilon", 0.0, 0.5)
        temperature = trial.suggest_float("temperature", 0.1, 1.5)

        utility_weights = {
            "prize_weight": trial.suggest_float("prize_weight", 0.5, 5.0),
            "hp_weight": trial.suggest_float("hp_weight", 0.1, 2.0),
            "energy_weight": trial.suggest_float("energy_weight", 0.1, 2.0),
            "bench_weight": trial.suggest_float("bench_weight", 0.1, 2.0),
            "win_weight": trial.suggest_float("win_weight", 10.0, 100.0),
        }

        return {
            "c_puct": c_puct,
            "exploration_rate": {
                "dirichlet_alpha": dirichlet_alpha,
                "dirichlet_epsilon": dirichlet_epsilon,
                "temperature": temperature,
            },
            "utility_weights": utility_weights,
        }

    @staticmethod
    def get_default_mcts_params() -> Dict[str, Any]:
        """Default baseline MCTS hyperparameter set."""
        return {
            "c_puct": 1.25,
            "exploration_rate": {
                "dirichlet_alpha": 0.3,
                "dirichlet_epsilon": 0.25,
                "temperature": 1.0,
            },
            "utility_weights": {
                "prize_weight": 2.0,
                "hp_weight": 1.0,
                "energy_weight": 1.0,
                "bench_weight": 0.5,
                "win_weight": 50.0,
            },
        }

    def create_study(self, direction: str = "maximize") -> Any:
        """Create or load an Optuna study."""
        if not OPTUNA_AVAILABLE:
            logger.error("Optuna is not available. Cannot create study.")
            return None
        return optuna.create_study(
            study_name=self.study_name,
            storage=self.storage,
            direction=direction,
            load_if_exists=True,
        )

    def optimize(
        self,
        eval_fn: Callable[[Dict[str, Any]], float],
        n_trials: int = 20,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Run Optuna study optimization given an evaluation callback.

        eval_fn receives hyperparameter dict (c_puct, exploration_rate, utility_weights)
        and returns a scalar score (higher is better for maximize).
        """
        if not OPTUNA_AVAILABLE:
            logger.warning("Optuna unavailable; returning default MCTS parameters.")
            return self.get_default_mcts_params()

        def objective(trial):
            params = self.sample_mcts_params(trial)
            return eval_fn(params)

        study = self.create_study(direction="maximize")
        if study is None:
            return self.get_default_mcts_params()

        study.optimize(objective, n_trials=n_trials, timeout=timeout)
        best_params = study.best_params

        # Reconstruct structured dict from flat Optuna trial parameters
        structured_best = {
            "c_puct": best_params.get("c_puct", 1.25),
            "exploration_rate": {
                "dirichlet_alpha": best_params.get("dirichlet_alpha", 0.3),
                "dirichlet_epsilon": best_params.get("dirichlet_epsilon", 0.25),
                "temperature": best_params.get("temperature", 1.0),
            },
            "utility_weights": {
                "prize_weight": best_params.get("prize_weight", 2.0),
                "hp_weight": best_params.get("hp_weight", 1.0),
                "energy_weight": best_params.get("energy_weight", 1.0),
                "bench_weight": best_params.get("bench_weight", 0.5),
                "win_weight": best_params.get("win_weight", 50.0),
            },
            "best_value": study.best_value,
        }

        self.save_best_params(structured_best)
        return structured_best

    def save_best_params(self, params: Dict[str, Any]):
        """Save best tuned MCTS parameters to disk."""
        try:
            self.best_params_path.parent.mkdir(parents=True, exist_ok=True)
            self.best_params_path.write_text(json.dumps(params, indent=2), encoding="utf-8")
            logger.info(f"Saved best Optuna MCTS parameters to {self.best_params_path}")
        except Exception as e:
            logger.warning(f"Failed to save best Optuna MCTS parameters: {e}")

    def load_best_params(self) -> Dict[str, Any]:
        """Load best tuned MCTS parameters from disk, or return defaults if absent."""
        if self.best_params_path.exists():
            try:
                return json.loads(self.best_params_path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning(f"Failed to load Optuna MCTS parameters from {self.best_params_path}: {e}")
        return self.get_default_mcts_params()


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
