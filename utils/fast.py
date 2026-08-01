
def fast(request):  # type: ignore[no-untyped-def]
    """--fast config option"""
    return request.config.getoption("--aiohttp-fast")

