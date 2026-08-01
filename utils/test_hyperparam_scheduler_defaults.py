
def test_hyperparam_scheduler_defaults():
    scheduler = HyperparamScheduler(total_iterations=100)
    
    # Test iteration 0
    hparams_0 = scheduler.get_all(0)
    assert hparams_0["learning_rate"] == pytest.approx(1e-3)
    assert hparams_0["entropy_coef"] == pytest.approx(0.08)
    assert hparams_0["c_puct"] == pytest.approx(1.25)
    assert hparams_0["clip_ratio"] == pytest.approx(0.2)
    assert "mcts_exploration_rate" in hparams_0
    assert "mcts_utility_weights" in hparams_0

    # Test iteration 100 (final)
    hparams_100 = scheduler.get_all(100)
    assert hparams_100["learning_rate"] == pytest.approx(1e-5)
    assert hparams_100["entropy_coef"] == pytest.approx(0.01)
    assert hparams_100["clip_ratio"] == pytest.approx(0.1)

