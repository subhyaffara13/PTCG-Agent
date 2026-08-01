
def test_optuna_mcts_tuner_save_load(tmp_path):
    tuner = OptunaMCTSTuner()
    tuner.best_params_path = tmp_path / "optuna_mcts_best.json"
    
    custom_params = {
        "c_puct": 1.8,
        "exploration_rate": {"dirichlet_alpha": 0.4, "dirichlet_epsilon": 0.2, "temperature": 0.9},
        "utility_weights": {"prize_weight": 3.0, "hp_weight": 1.2, "energy_weight": 0.8, "bench_weight": 0.6, "win_weight": 60.0},
        "best_value": 0.85
    }
    tuner.save_best_params(custom_params)
    
    loaded = tuner.load_best_params()
    assert loaded["c_puct"] == 1.8
    assert loaded["exploration_rate"]["dirichlet_alpha"] == 0.4
    assert loaded["utility_weights"]["prize_weight"] == 3.0

