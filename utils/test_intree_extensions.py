
def test_intree_extensions(monkeypatch, tmpdir):
    monkeypatch.syspath_prepend(MAIN_DIR)

    from pybind11.setup_helpers import intree_extensions

    monkeypatch.chdir(tmpdir)
    root = tmpdir
    root.ensure_dir()
    subdir = root / "dir"
    subdir.ensure_dir()
    src = subdir / "ext.cpp"
    src.ensure()
    relpath = src.relto(tmpdir)
    (ext,) = intree_extensions([relpath])
    assert ext.name == "ext"
    subdir.ensure("__init__.py")
    (ext,) = intree_extensions([relpath])
    assert ext.name == "dir.ext"

