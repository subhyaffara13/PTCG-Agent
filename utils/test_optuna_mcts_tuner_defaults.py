
def test_optuna_mcts_tuner_defaults():
    tuner = OptunaMCTSTuner()
    defaults = tuner.get_default_mcts_params()
    assert "c_puct" in defaults
    assert "exploration_rate" in defaults
    assert "utility_weights" in defaults
    assert defaults["c_puct"] == 1.25
    assert defaults["exploration_rate"]["dirichlet_alpha"] == 0.3
    assert defaults["utility_weights"]["prize_weight"] == 2.0

