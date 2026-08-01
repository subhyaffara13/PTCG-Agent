
def wheel_paths(tmp_path_factory):
    build_base = tmp_path_factory.mktemp("build")
    dist_dir = tmp_path_factory.mktemp("dist")
    for name in EXAMPLES:
        example_dir = mkexample(tmp_path_factory, name)
        build_dir = build_base / name
        with jaraco.path.DirectoryStack().context(example_dir):
            bdist_wheel_cmd(bdist_dir=str(build_dir), dist_dir=str(dist_dir)).run()

    return sorted(str(fname) for fname in dist_dir.glob("*.whl"))

