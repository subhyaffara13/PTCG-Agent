
def test_dist_default_py_modules(tmp_path, dist_name, py_module):
    (tmp_path / f"{py_module}.py").touch()

    (tmp_path / "setup.py").touch()
    (tmp_path / "noxfile.py").touch()
    # ^-- make sure common tool files are ignored

    attrs = {**EXAMPLE_BASE_INFO, "name": dist_name, "src_root": str(tmp_path)}
    # Find `py_modules` corresponding to dist_name if not given
    dist = Distribution(attrs)
    dist.set_defaults()
    assert dist.py_modules == [py_module]
    # When `py_modules` is given, don't do anything
    dist = Distribution({**attrs, "py_modules": ["explicity_py_module"]})
    dist.set_defaults()
    assert dist.py_modules == ["explicity_py_module"]
    # When `packages` is given, don't do anything
    dist = Distribution({**attrs, "packages": ["explicity_package"]})
    dist.set_defaults()
    assert not dist.py_modules

