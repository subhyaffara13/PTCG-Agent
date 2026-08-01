
def instance_caches() -> Generator[InstanceCacheInspector, None, None]:
    """
    Fixture to ensure empty filesystem instance caches before and after a test.

    Used by default for all tests.
    Clears caches of all imported filesystem classes.
    Can be used to write test assertions about instance caches.

    Usage:

        def test_something(instance_caches):
            # Test code here
            fsspec.open("file://abc")
            fsspec.open("memory://foo/bar")

            # Test assertion
            assert instance_caches.gather_counts() == {"file": 1, "memory": 1}

    Returns
    -------
    instance_caches: An instance cache inspector for clearing and inspecting caches.
    """
    ic = InstanceCacheInspector()

    ic.clear()
    try:
        yield ic
    finally:
        ic.clear()

