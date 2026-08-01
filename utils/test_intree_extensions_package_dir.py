
def test_intree_extensions_package_dir(monkeypatch, tmpdir):
    monkeypatch.syspath_prepend(MAIN_DIR)

    from pybind11.setup_helpers import intree_extensions

    monkeypatch.chdir(tmpdir)
    root = tmpdir / "src"
    root.ensure_dir()
    subdir = root / "dir"
    subdir.ensure_dir()
    src = subdir / "ext.cpp"
    src.ensure()
    (ext,) = intree_extensions([src.relto(tmpdir)], package_dir={"": "src"})
    assert ext.name == "dir.ext"
    (ext,) = intree_extensions([src.relto(tmpdir)], package_dir={"foo": "src"})
    assert ext.name == "foo.dir.ext"
    subdir.ensure("__init__.py")
    (ext,) = intree_extensions([src.relto(tmpdir)], package_dir={"": "src"})
    assert ext.name == "dir.ext"
    (ext,) = intree_extensions([src.relto(tmpdir)], package_dir={"foo": "src"})
    assert ext.name == "foo.dir.ext"

