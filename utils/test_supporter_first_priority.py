
def test_supporter_first_priority(tmp_path):
    setup_skills_dir(tmp_path, "priority_rules.json", PRIORITY_RULES_EMPTY)
    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(tmp_path / "skills"))
    packet = TurnPlannerPacket(hand_score=0.5, priority_profile="aggro_push", top_play="none", game_state={
        "legal_trainers": ["Ultra Ball", "Professor's Research", "Pok\u00e9 Ball"],
        "my_active_pokemon": None, "my_hand": [1, 2, 3, 4]
    }, turn=1)
    trainers = [a for a in planner.receive(packet)["action_sequence"] if a.startswith("play_trainer:")]
    assert trainers[0] == "play_trainer:Professor's Research"

