
def test_find_packages(tmp_path, args, pkgs):
    files = {
        "pkg/__init__.py",
        "other/__init__.py",
        "dir1/dir2/__init__.py",
    }
    write_files({k: "" for k in files}, tmp_path)

    package_dir = {}
    kwargs = {"root_dir": tmp_path, "fill_package_dir": package_dir, **args}
    where = kwargs.get("where", ["."])
    assert set(expand.find_packages(**kwargs)) == pkgs
    for pkg in pkgs:
        pkg_path = find_package_path(pkg, package_dir, tmp_path)
        assert os.path.exists(pkg_path)

    # Make sure the same APIs work outside cwd
    where = [
        str((tmp_path / p).resolve()).replace(os.sep, "/")  # ensure posix-style paths
        for p in args.pop("where", ["."])
    ]

    assert set(expand.find_packages(where=where, **args)) == pkgs

