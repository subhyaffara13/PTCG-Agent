
def set_current_async_library(asynclib_name: str | None) -> Token | None:
    # no-op if sniffio is not installed
    if sniffio is None:
        return None

    return sniffio.current_async_library_cvar.set(asynclib_name)

