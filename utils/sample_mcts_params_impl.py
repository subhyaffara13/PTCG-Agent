from typing import Any, Dict

def sample_mcts_params_impl(trial: Any) -> Dict[str, Any]:
    if not OPTUNA_AVAILABLE or trial is None:
        return get_default_mcts_params_impl()
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
    return {"c_puct": c_puct, "exploration_rate": {"dirichlet_alpha": dirichlet_alpha, "dirichlet_epsilon": dirichlet_epsilon, "temperature": temperature}, "utility_weights": utility_weights}

