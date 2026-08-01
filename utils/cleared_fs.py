
def cleared_fs():
    fsspec = pytest.importorskip("fsspec")

    memfs = fsspec.filesystem("memory")
    yield memfs
    memfs.store.clear()

