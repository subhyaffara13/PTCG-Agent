
def ensure_event_loop(prefer_selector_loop: bool = False) -> asyncio.AbstractEventLoop:
    # Get the loop for this thread, or create a new one.
    loop = _loop.get()
    if loop is not None and not loop.is_closed():
        return loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        if sys.platform == "win32" and prefer_selector_loop:
            if (3, 14) <= sys.version_info < (3, 15):
                # ignore deprecation only for 3.14 and revisit later.
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore",
                        category=DeprecationWarning,
                        message=".*WindowsSelectorEventLoopPolicy.*",
                    )
                    loop = asyncio.WindowsSelectorEventLoopPolicy().new_event_loop()
            else:
                loop = asyncio.WindowsSelectorEventLoopPolicy().new_event_loop()
        else:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    _loop.set(loop)
    return loop

