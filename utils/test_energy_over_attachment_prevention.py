
def test_energy_over_attachment_prevention(tmp_path):
    setup_skills_dir(tmp_path, "priority_rules.json", PRIORITY_RULES_EMPTY)
    planner = TurnPlanner(log_dir=str(tmp_path), skills_dir=str(tmp_path / "skills"))
    packet = TurnPlannerPacket(hand_score=0.8, priority_profile="aggro_push", top_play="none", game_state={
        "legal_attachments": ["Active"], "legal_attacks": ["Thunderbolt"],
        "my_active_pokemon": CHARGED_ACTIVE
    }, turn=1)
    seq = planner.receive(packet)["action_sequence"]
    assert seq.index("attack:Thunderbolt") < seq.index("attach_energy:Active")

