
def get_default_mcts_params_impl() -> Dict[str, Any]:
    return {"c_puct": 1.25, "exploration_rate": {"dirichlet_alpha": 0.3, "dirichlet_epsilon": 0.25, "temperature": 1.0},
            "utility_weights": {"prize_weight": 2.0, "hp_weight": 1.0, "energy_weight": 1.0, "bench_weight": 0.5, "win_weight": 50.0}}

