import pytest
from unittest.mock import patch, MagicMock
from cb_agents.mcts_engine import MCTSEngine

def test_mcts_fallback_when_import_fails():
    # If ptcg_core is not present or we mock HAS_CPP as False
    with patch("agents.mcts_engine.HAS_CPP", False):
        engine = MCTSEngine(num_simulations=5)
        # Mock _evaluate_state to avoid running full value network
        engine._evaluate_state = MagicMock(return_value=0.5)
        
        game_state = {
            "my_hand": ["Energy"],
            "my_deck_count": 40,
            "my_prizes": 6,
            "turn_number": 1,
        }
        legal_actions = ["bench:Energy", "pass"]
        
        # This should execute python MCTS without throwing import error
        action = engine.search(game_state, legal_actions)
        assert action in legal_actions

def test_mcts_fallback_when_cpp_raises_exception():
    mock_ptcg_core = MagicMock()
    mock_ptcg_core.mcts_search.side_effect = RuntimeError("MCTS crash")
    
    with patch("agents.mcts_engine.ptcg_core", mock_ptcg_core), \
         patch("agents.mcts_engine.HAS_CPP", True):
         
        engine = MCTSEngine(num_simulations=5)
        engine._evaluate_state = MagicMock(return_value=0.5)
        
        game_state = {
            "my_hand": ["Energy"],
            "my_deck_count": 40,
            "my_prizes": 6,
            "turn_number": 1,
        }
        legal_actions = ["bench:Energy", "pass"]
        
        # It should catch the RuntimeError and fallback to Python search
        action = engine.search(game_state, legal_actions)
        assert action in legal_actions
        assert mock_ptcg_core.mcts_search.called
