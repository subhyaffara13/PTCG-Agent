
def _portable_async_sleep(seconds: float) -> t.Awaitable[None]:
    # If trio is already imported, then importing it is cheap.
    # If trio isn't already imported, then it's definitely not running, so we
    # can skip further checks.
    if "trio" in sys.modules:
        # If trio is available, then sniffio is too
        import trio
        import sniffio

        if sniffio.current_async_library() == "trio":
            return trio.sleep(seconds)
    # Otherwise, assume asyncio
    # Lazy import asyncio as it's expensive (responsible for 25-50% of total import overhead).
    import asyncio

    return asyncio.sleep(seconds)

