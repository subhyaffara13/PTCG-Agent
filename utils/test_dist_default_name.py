
def test_dist_default_name(tmp_path, dist_name, package_dir, package_files):
    """Make sure dist.name is discovered from packages/py_modules"""
    ensure_files(tmp_path, package_files)
    attrs = {
        **EXAMPLE_BASE_INFO,
        "src_root": "/".join(os.path.split(tmp_path)),  # POSIX-style
        "package_dir": package_dir,
    }
    del attrs["name"]

    dist = Distribution(attrs)
    dist.set_defaults()
    assert dist.py_modules or dist.packages
    assert dist.get_name() == dist_name

