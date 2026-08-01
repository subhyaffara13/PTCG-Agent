
def test_prized_attacker_strategy_switch(tmp_path):
    setup_skills_dir(tmp_path, "strategy_profiles.json", STRATEGY_PROFILES_EMPTY)
    agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(tmp_path / "skills"))
    res = agent.receive(StrategyPacket(trigger="turn_start", board_summary={
        "my_prizes_remaining": 6, "opponent_prizes_remaining": 6,
        "opponent_confidence": 0.1, "priority_profile": "aggro_push",
        "turn_number": 2, "prized_probabilities": {"721": 0.85}
    }))
    assert res["strategy"] == "setup"

