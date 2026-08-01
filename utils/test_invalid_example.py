
def test_invalid_example(tmp_path, example, error_msg):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(cleandoc(example), encoding="utf-8")

    pattern = re.compile(
        f"invalid pyproject.toml.*{error_msg}.*", re.MULTILINE | re.DOTALL
    )
    with pytest.raises(ValueError, match=pattern):
        read_configuration(pyproject)

