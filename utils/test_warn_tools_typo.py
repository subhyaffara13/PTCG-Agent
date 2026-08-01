
def test_warn_tools_typo(tmp_path):
    """Test that the common ``tools.setuptools`` typo in ``pyproject.toml`` issues a warning

    See https://github.com/pypa/setuptools/issues/4150
    """
    config = """
    [build-system]
    requires = ["setuptools"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "myproj"
    version = '42'

    [tools.setuptools]
    packages = ["package"]
    """

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(cleandoc(config), encoding="utf-8")

    with pytest.warns(_ToolsTypoInMetadata):
        read_configuration(pyproject)

