from . import Any, Callable, Dict, OPTUNA_AVAILABLE, Optional, Path, json, logger, optuna

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

