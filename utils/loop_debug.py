
def loop_debug(request):  # type: ignore[no-untyped-def]
    """--enable-loop-debug config option"""
    return request.config.getoption("--aiohttp-enable-loop-debug")

