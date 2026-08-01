
def test_ignore_unrelated_config(tmp_path, example):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(cleandoc(example), encoding="utf-8")

    # Make sure no error is raised due to 3rd party configs in pyproject.toml
    assert read_configuration(pyproject) is not None

