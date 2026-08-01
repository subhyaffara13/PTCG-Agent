
def test_read_configuration(tmp_path):
    create_example(tmp_path, "src")
    pyproject = tmp_path / "pyproject.toml"

    config = read_configuration(pyproject, expand=False)
    assert config["project"].get("version") is None
    assert config["project"].get("readme") is None

    verify_example(config, tmp_path, "src")

