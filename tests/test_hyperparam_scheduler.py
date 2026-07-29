"""
tests/test_hyperparam_scheduler.py

Unit tests for HyperparamScheduler and OptunaMCTSTuner.
"""
import pytest
from factory.hyperparam_scheduler import HyperparamScheduler, OptunaMCTSTuner


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


def test_optuna_mcts_tuner_defaults():
    tuner = OptunaMCTSTuner()
    defaults = tuner.get_default_mcts_params()
    assert "c_puct" in defaults
    assert "exploration_rate" in defaults
    assert "utility_weights" in defaults
    assert defaults["c_puct"] == 1.25
    assert defaults["exploration_rate"]["dirichlet_alpha"] == 0.3
    assert defaults["utility_weights"]["prize_weight"] == 2.0


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
