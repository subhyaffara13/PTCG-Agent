
def test_client(aiohttp_client):  # type: ignore[no-untyped-def]  # pragma: no cover
    warnings.warn(
        "Deprecated, use aiohttp_client fixture instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return aiohttp_client

