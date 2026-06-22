"""
tests/test_shared_context.py

Unit tests for agents/context.py (SharedContext singleton cache manager).
"""

import json
from pathlib import Path
from agents.context import SharedContext
from agents.orchestrator import Orchestrator

def test_shared_context_singleton(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # Write a test config
    config_file = skills_dir / "priority_rules.json"
    rules_data = {"rules": [{"test": "value"}]}
    config_file.write_text(json.dumps(rules_data), encoding="utf-8")
    
    # Get instances
    ctx1 = SharedContext()
    ctx2 = SharedContext()
    
    assert ctx1 is ctx2
    
    # Load config and verify it returns correct content
    loaded = ctx1.get_config(str(skills_dir), "priority_rules.json")
    assert loaded == rules_data
    
    # Mutate data in file to check if cache returns cached value
    config_file.write_text(json.dumps({"rules": []}), encoding="utf-8")
    loaded_cached = ctx2.get_config(str(skills_dir), "priority_rules.json")
    assert loaded_cached == rules_data  # returns cached, does not read disk again

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
    assert orchestrator.hand_analyst.shared_context is orchestrator.context
    assert orchestrator.turn_planner.shared_context is orchestrator.context
    assert orchestrator.strategy_agent.shared_context is orchestrator.context
    assert orchestrator.opponent_model.shared_context is orchestrator.context
