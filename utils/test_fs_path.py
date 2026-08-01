
def test_fs_path():
    from pathlib import Path

    class PseudoStrPath:
        def __fspath__(self):
            return "foo/bar"

    class PseudoBytesPath:
        def __fspath__(self):
            return b"foo/bar"

    assert m.parent_path(Path("foo/bar")) == Path("foo")
    assert m.parent_path("foo/bar") == Path("foo")
    assert m.parent_path(b"foo/bar") == Path("foo")
    assert m.parent_path(PseudoStrPath()) == Path("foo")
    assert m.parent_path(PseudoBytesPath()) == Path("foo")

