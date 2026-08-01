
def test_eval_agent_evaluate_fallback(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    rubric_file = skills_dir / "eval_rubric.json"
    rubric_file.write_text(json.dumps({"contexts": {}}), encoding="utf-8")
    
    agent = EvalAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    # Empty iteration result should score as 0.0 without throwing
    res = agent.evaluate({"iteration": 1, "games": {}})
    
    assert res["iteration"] == 1
    assert res["adjusted_scores"]["reasoning_test"] == 0.0
    assert (tmp_path / "eval_report.json").exists()
    assert (tmp_path / "eval_state.json").exists()

