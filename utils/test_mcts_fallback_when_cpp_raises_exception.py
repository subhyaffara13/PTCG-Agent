
def test_mcts_fallback_when_cpp_raises_exception():
    mock_ptcg_core = MagicMock()
    mock_ptcg_core.mcts_search.side_effect = RuntimeError("MCTS crash")
    
    with patch("cb_agents.mcts_engine.mctsengine.ptcg_core", mock_ptcg_core), \
         patch("cb_agents.mcts_engine.mctsengine.HAS_CPP", True), \
         patch("cb_agents.mcts_engine.mctsengine.pipeline") as mock_pipeline:
        # Ensure mask_actions passes through so we actually reach the C++ path
        mock_pipeline.mask_actions.return_value = (["bench:Charmander", "pass"], [])
         
        engine = MCTSEngine(num_simulations=5)
        engine._evaluate_state = MagicMock(return_value=0.5)
        
        game_state = {
            "my_hand": ["Charmander", "Energy"],
            "my_deck_count": 40,
            "my_prizes": 6,
            "turn_number": 1,
        }
        legal_actions = ["bench:Charmander", "pass"]
        
        # It should catch the RuntimeError and fallback to Python search
        action = engine.search(game_state, legal_actions)
        assert action in legal_actions
        assert mock_ptcg_core.mcts_search.called

