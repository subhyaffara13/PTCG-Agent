import json

def test_eval_agent_context_resolution(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
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

    agent = EvalAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    ctx = agent._determine_context("deck_swap", "")
    assert ctx == "deck_test"
    
    ctx_strategy = agent._determine_context("strategy_patch", "aggro")
    assert ctx_strategy == "aggro_test"

