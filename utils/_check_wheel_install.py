
def _check_wheel_install(
    filename, install_dir, install_tree_includes, project_name, version, requires_txt
):
    w = Wheel(filename)
    egg_path = os.path.join(install_dir, w.egg_name())
    w.install_as_egg(egg_path)
    if install_tree_includes is not None:
        install_tree = format_install_tree(install_tree_includes)
        exp = tree_set(install_dir)
        assert install_tree.issubset(exp), install_tree - exp

    (dist,) = metadata.Distribution.discover(path=[egg_path])

    # pyright is nitpicky; fine to assume dist.metadata.__getitem__ will fail or return None
    # (https://github.com/pypa/setuptools/pull/5006#issuecomment-2894774288)
    assert dist.metadata['Name'] == project_name  # pyright: ignore  # noqa: PGH003
    assert dist.metadata['Version'] == version  # pyright: ignore  # noqa: PGH003
    assert dist.read_text('requires.txt') == requires_txt

