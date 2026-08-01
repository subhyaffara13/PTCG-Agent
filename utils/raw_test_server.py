
def raw_test_server(  # type: ignore[no-untyped-def]  # pragma: no cover
    aiohttp_raw_server,
):
    warnings.warn(
        "Deprecated, use aiohttp_raw_server fixture instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return aiohttp_raw_server

