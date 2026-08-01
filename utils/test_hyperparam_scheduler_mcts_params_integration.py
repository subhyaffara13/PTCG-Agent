
def test_hyperparam_scheduler_mcts_params_integration(tmp_path):
    scheduler = HyperparamScheduler(total_iterations=100)
    scheduler.optuna_tuner.best_params_path = tmp_path / "optuna_mcts_best.json"
    
    # Standard schedule
    mcts_params = scheduler.get_mcts_params(iteration=50, use_optuna=False)
    assert mcts_params["c_puct"] < 1.25

    # Saved optuna params integration
    custom_params = {
        "c_puct": 2.1,
        "exploration_rate": {"dirichlet_alpha": 0.2, "dirichlet_epsilon": 0.15, "temperature": 0.8},
        "utility_weights": {"prize_weight": 2.5, "hp_weight": 1.5, "energy_weight": 1.1, "bench_weight": 0.4, "win_weight": 75.0}
    }
    scheduler.optuna_tuner.save_best_params(custom_params)

    optuna_mcts_params = scheduler.get_mcts_params(iteration=50, use_optuna=True)
    assert optuna_mcts_params["c_puct"] == 2.1
    assert optuna_mcts_params["utility_weights"]["win_weight"] == 75.0

