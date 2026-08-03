import json

def test_orchestrator_context_injection(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Save required config files
    (skills_dir / "priority_rules.json").write_text(json.dumps({"rules": []}), encoding="utf-8")
    (skills_dir / "strategy_profiles.json").write_text(json.dumps({"profiles": {}}), encoding="utf-8")
    (skills_dir / "deck_archetypes.json").write_text(json.dumps({"archetypes": {}}), encoding="utf-8")
    (skills_dir / "card_scoring.json").write_text(json.dumps({"cards": []}), encoding="utf-8")
    (skills_dir / "delegation_map.json").write_text(json.dumps({"delegation": {}}), encoding="utf-8")

    orchestrator = Orchestrator(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    # Verify sub-agents got the context injected
    assert orchestrator.context is not None
    assert getattr(orchestrator, "hand_analyst", getattr(orchestrator, "_analyst", None)).shared_context is orchestrator.context
    assert getattr(orchestrator, "turn_planner", getattr(orchestrator, "_planner", None)).shared_context is orchestrator.context
    assert getattr(orchestrator, "strategy_agent", getattr(orchestrator, "_strategy", None)).shared_context is orchestrator.context
    assert getattr(orchestrator, "opponent_model", getattr(orchestrator, "_opponent", None)).shared_context is orchestrator.context

