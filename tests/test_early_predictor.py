"""
tests/test_early_predictor.py

Unit tests for factory/early_predictor.py.
"""

import json
import pytest
from pathlib import Path
from factory.early_predictor import EarlyWinPredictor

def test_early_win_predictor(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()

    predictor = EarlyWinPredictor(skills_dir=str(skills_dir))
    
    # Verify default weights loaded
    assert predictor.weights["prize_weight"] == 2.0
    assert predictor.weights["hand_weight"] == 0.5

    # Mock deck and steps up to turn 5
    # Observation contains players array with prize, hand, active, bench details
    mock_steps = [
        {
            "step": 0,
            "players": [
                {
                    "observation": {
                        "current": {
                            "turn": 1,
                            "players": [
                                {"prize": [1, 2, 3, 4, 5, 6], "hand": [1, 2, 3], "active": [{"hp": 60, "attached": []}], "bench": []},
                                {"prize": [1, 2, 3, 4, 5, 6], "hand": [1, 2, 3], "active": [{"hp": 60, "attached": []}], "bench": []}
                            ]
                        }
                    }
                },
                {
                    "observation": {}
                }
            ]
        },
        {
            "step": 1,
            "players": [
                {
                    "observation": {
                        "current": {
                            "turn": 4,
                            # Player A is doing much better: took 2 prizes, has benched pokemon and attached energy
                            "players": [
                                {"prize": [1, 2, 3, 4], "hand": [1, 2, 3, 4], "active": [{"hp": 100, "attached": [1, 2]}], "bench": [{"id": 5}]},
                                {"prize": [1, 2, 3, 4, 5, 6], "hand": [1, 2], "active": [{"hp": 50, "attached": []}], "bench": []}
                            ]
                        }
                    }
                },
                {
                    "observation": {}
                }
            ]
        }
    ]

    # Predict winner
    prediction = predictor.predict_winner([], [], mock_steps)
    # Player A should be predicted since they took prizes and have more active/bench/energy presence
    assert prediction == "player_a"

    # Test upgrade on wrong prediction
    # Predictor predicted "player_a", but actual winner is "player_b"
    predictor.upgrade(prediction, "player_b", mock_steps)
    
    # Weights should be adjusted
    assert predictor.weights != predictor._load_weights
    
    # Check that feedback log has been written
    feedback_file = skills_dir / "predictor_feedback.json"
    assert feedback_file.exists()
    
    feedbacks = json.loads(feedback_file.read_text(encoding="utf-8"))
    assert len(feedbacks) == 1
    assert feedbacks[0]["prediction"] == "player_a"
    assert feedbacks[0]["actual"] == "player_b"
