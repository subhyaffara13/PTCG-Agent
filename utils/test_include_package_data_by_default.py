
def test_include_package_data_by_default(tmp_path, config):
    """Builds with ``pyproject.toml`` should consider ``include-package-data=True`` as
    default.
    """
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(config, encoding="utf-8")

    config = read_configuration(pyproject)
    assert config["tool"]["setuptools"]["include-package-data"] is True

