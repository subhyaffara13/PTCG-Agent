"""
tests/test_builder_agent.py

Unit tests for factory/builder_agent.py.
"""

import os
import json
import pytest
from pathlib import Path
from factory.builder_agent import BuilderAgent

def test_builder_agent_unauthorized_target(tmp_path):
    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n", encoding="utf-8")
    
    agent = BuilderAgent(
        log_dir=str(tmp_path),
        staging_dir=str(tmp_path / "staging"),
        decisions_file=str(decisions_file)
    )

    notes = {
        "iteration": 1,
        "escalation": {"target": "cb_agents/orchestrator.py"},
        "reasoning": "Tuning logic",
        "action_taken": "logic_delta"
    }

    res = agent.build(notes)
    
    assert res["status"] == "failed"
    assert res["reason"] == "unauthorized_target"
    
    content = decisions_file.read_text(encoding="utf-8")
    assert "BUILDER AGENT ERROR" in content
