
def test_validator_syntax_check(tmp_path):
    versions_dir = tmp_path / "versions"
    staging_dir = tmp_path / "staging"
    agents_dir = tmp_path / "agents"
    factory_dir = tmp_path / "factory"
    
    versions_dir.mkdir()
    staging_dir.mkdir()
    agents_dir.mkdir()
    factory_dir.mkdir()

    agent = ValidatorAgent(
        log_dir=str(tmp_path),
        versions_dir=str(versions_dir),
        staging_dir=str(staging_dir),
        agents_dir=str(agents_dir),
        factory_dir=str(factory_dir)
    )

    # Write code with bad syntax
    staged = staging_dir / "bad_agent.py"
    staged.write_text("class BadAgent:\n    def receive(self): \n  invalid syntax here !!!", encoding="utf-8")

    eval_report = {"version_scores": {"player_b": 0.5}}

    res = agent.validate(str(staged), eval_report)
    
    assert res["all_passed"] is False
    assert res["checks"]["syntax"] == "fail"
    assert res["failed_check"] == "check_1"

