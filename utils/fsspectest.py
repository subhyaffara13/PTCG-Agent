
def fsspectest():
    pytest.importorskip("fsspec")
    from fsspec import register_implementation
    from fsspec.implementations.memory import MemoryFileSystem
    from fsspec.registry import _registry as registry

    class TestMemoryFS(MemoryFileSystem):
        protocol = "testmem"
        test = [None]

        def __init__(self, **kwargs) -> None:
            self.test[0] = kwargs.pop("test", None)
            super().__init__(**kwargs)

    register_implementation("testmem", TestMemoryFS, clobber=True)
    yield TestMemoryFS()
    registry.pop("testmem", None)
    TestMemoryFS.test[0] = None
    TestMemoryFS.store.clear()

