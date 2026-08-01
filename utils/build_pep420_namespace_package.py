
def build_pep420_namespace_package(tmpdir, name):
    src_dir = tmpdir / name
    src_dir.mkdir()
    pyproject = src_dir / "pyproject.toml"
    namespace, _, rest = name.rpartition(".")
    script = f"""\
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "{name}"
        version = "3.14159"
        """
    pyproject.write_text(textwrap.dedent(script), encoding='utf-8')
    ns_pkg_dir = Path(src_dir, namespace.replace(".", "/"))
    ns_pkg_dir.mkdir(parents=True)
    pkg_mod = ns_pkg_dir / (rest + ".py")
    some_functionality = f"name = {rest!r}"
    pkg_mod.write_text(some_functionality, encoding='utf-8')
    return src_dir

