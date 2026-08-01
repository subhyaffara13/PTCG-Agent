
def test_server(aiohttp_server):  # type: ignore[no-untyped-def]  # pragma: no cover
    warnings.warn(
        "Deprecated, use aiohttp_server fixture instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return aiohttp_server

