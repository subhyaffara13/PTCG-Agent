
def test_game_logger_logging_functions(tmp_path):
    gl = GameLogger(log_dir=str(tmp_path))
    gl.log_action(1, "strategy_agent", "on_trigger", {"cards": []}, {"cards": ["A"]})
    gl.log_reasoning(1, "aggro", 8.5, False, 0.45, "Chain text", True, "positive")
    gl.log_variance(1, "coin_flip", "heads", "tails", -1.0)
    
    assert len(gl.action_logs) == 1
    assert len(gl.reasoning_logs) == 1
    assert len(gl.variance_logs) == 1
    
    assert gl.action_logs[0]["turn"] == 1
    assert gl.reasoning_logs[0]["reasoning_outcome"] == "positive"
    assert gl.variance_logs[0]["event_type"] == "coin_flip"

