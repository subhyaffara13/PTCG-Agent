
def reset_current_async_library(token: Token | None) -> None:
    if token is not None:
        sniffio.current_async_library_cvar.reset(token)

