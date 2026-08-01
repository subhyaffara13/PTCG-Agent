
def test_game_logger_save_creates_files(tmp_path):
    gl = GameLogger(log_dir=str(tmp_path))
    gl.log_action(1, "strategy_agent", "on_trigger", {"cards": []}, {"cards": ["A"]})
    gl.log_reasoning(1, "aggro", 8.5, False, 0.45, "Chain text", True, "positive")
    gl.log_variance(1, "coin_flip", "heads", "tails", -1.0)
    
    gl.save("base_v1", "new_v2")
    
    # Assert files are created
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 3
    
    # Check naming conventions
    prefixes = {f.name.split("_")[0] for f in files}
    assert prefixes == {"action", "reasoning", "variance"}
    
    for f in files:
        assert "base_v1_vs_vnew_v2" in f.name

