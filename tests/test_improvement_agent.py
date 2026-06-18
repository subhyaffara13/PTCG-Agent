"""
tests/test_improvement_agent.py

Unit tests for factory/improvement_agent.py.
"""

import os
import json
import pytest
from pathlib import Path
from factory.improvement_agent import ImprovementAgent

def test_improvement_agent_tune_logic(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    decisions_file = tmp_path / "decisions.md"
    decisions_file.write_text("# Decisions\n", encoding="utf-8")
    
    rubric_file = skills_dir / "eval_rubric.json"
    rubric_file.write_text(json.dumps({
        "contexts": {
            "aggro_test": {
                "win_rate": 0.35,
                "prize_efficiency": 0.25,
                "turn_efficiency": 0.00,
                "ko_rate": 0.20,
                "logic_delta": 0.20
            }
        }
    }), encoding="utf-8")

    agent = ImprovementAgent(
        log_dir=str(tmp_path),
        skills_dir=str(skills_dir),
        decisions_file=str(decisions_file)
    )

    eval_report = {
        "iteration": 1,
        "eval_context": "aggro_test",
        "recommendation": "tune",
        "metrics": {
            "logic_delta": 0.05,
            "deck_delta": 0.5
        },
        "flags": {
            "flag_deck_architect": False,
            "flag_builder_agent": False
        },
        "version_scores": {
            "best_version": "player_b"
        }
    }

    res = agent.improve(eval_report)
    
    assert res["action_taken"] == "tuned_weights"
    assert (tmp_path / "improvement_notes.json").exists()
    
    # Verify decisions.md append
    content = decisions_file.read_text(encoding="utf-8")
    assert "## Iteration 1" in content
