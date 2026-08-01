
def test_discovered_package_dir_with_attr_directive_in_config(tmp_path, pkg_root, opts):
    create_example(tmp_path, pkg_root)

    pyproject = tmp_path / "pyproject.toml"

    config = read_configuration(pyproject, expand=False)
    assert config["project"].get("version") is None
    assert config["project"].get("readme") is None
    config["tool"]["setuptools"].pop("packages", None)
    config["tool"]["setuptools"].pop("package-dir", None)

    config["tool"]["setuptools"].update(opts)
    verify_example(config, tmp_path, pkg_root)

