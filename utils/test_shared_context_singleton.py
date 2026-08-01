
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

