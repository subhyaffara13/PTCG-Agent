import os

def test_fill_package_dir(tmp_path, files, where, expected_package_dir):
    write_files({k: "" for k in files}, tmp_path)
    pkg_dir = {}
    kwargs = {"root_dir": tmp_path, "fill_package_dir": pkg_dir, "namespaces": False}
    pkgs = expand.find_packages(where=where, **kwargs)
    assert set(pkg_dir.items()) == set(expected_package_dir.items())
    for pkg in pkgs:
        pkg_path = find_package_path(pkg, pkg_dir, tmp_path)
        assert os.path.exists(pkg_path)

