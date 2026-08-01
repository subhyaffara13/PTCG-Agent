
def test_dist_default_packages(
    tmp_path, dist_name, package_dir, package_files, packages
):
    ensure_files(tmp_path, package_files)

    (tmp_path / "setup.py").touch()
    (tmp_path / "noxfile.py").touch()
    # ^-- should not be included by default

    attrs = {
        **EXAMPLE_BASE_INFO,
        "name": dist_name,
        "src_root": str(tmp_path),
        "package_dir": package_dir,
    }
    # Find `packages` either corresponding to dist_name or inside src
    dist = Distribution(attrs)
    dist.set_defaults()
    assert not dist.py_modules
    assert not dist.py_modules
    assert set(dist.packages) == set(packages)
    # When `py_modules` is given, don't do anything
    dist = Distribution({**attrs, "py_modules": ["explicit_py_module"]})
    dist.set_defaults()
    assert not dist.packages
    assert set(dist.py_modules) == {"explicit_py_module"}
    # When `packages` is given, don't do anything
    dist = Distribution({**attrs, "packages": ["explicit_package"]})
    dist.set_defaults()
    assert not dist.py_modules
    assert set(dist.packages) == {"explicit_package"}

