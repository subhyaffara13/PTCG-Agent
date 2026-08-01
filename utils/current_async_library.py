
def current_async_library() -> str:
    # Determine if we're running under trio or asyncio.
    # See https://sniffio.readthedocs.io/en/latest/
    try:
        import sniffio
    except ImportError:  # pragma: nocover
        environment = "asyncio"
    else:
        environment = sniffio.current_async_library()

    if environment not in ("asyncio", "trio"):  # pragma: nocover
        raise RuntimeError("Running under an unsupported async environment.")

    if environment == "asyncio" and anyio is None:  # pragma: nocover
        raise RuntimeError(
            "Running with asyncio requires installation of 'httpcore[asyncio]'."
        )

    if environment == "trio" and trio is None:  # pragma: nocover
        raise RuntimeError(
            "Running with trio requires installation of 'httpcore[trio]'."
        )

    return environment


def current_async_library() -> str:
    """Detect which async library is currently running.

    The following libraries are currently supported:

    ================   ===========  ============================
    Library             Requires     Magic string
    ================   ===========  ============================
    **Trio**            Trio v0.6+   ``"trio"``
    **Curio**           -            ``"curio"``
    **asyncio**                      ``"asyncio"``
    **Trio-asyncio**    v0.8.2+     ``"trio"`` or ``"asyncio"``,
                                    depending on current mode
    ================   ===========  ============================

    Returns:
      A string like ``"trio"``.

    Raises:
      AsyncLibraryNotFoundError: if called from synchronous context,
        or if the current async library was not recognized.

    Examples:

        .. code-block:: python3

           from sniffio import current_async_library

           async def generic_sleep(seconds):
               library = current_async_library()
               if library == "trio":
                   import trio
                   await trio.sleep(seconds)
               elif library == "asyncio":
                   import asyncio
                   await asyncio.sleep(seconds)
               # ... and so on ...
               else:
                   raise RuntimeError(f"Unsupported library {library!r}")

    """
    value = thread_local.name
    if value is not None:
        return value

    value = current_async_library_cvar.get()
    if value is not None:
        return value

    # Need to sniff for asyncio
    if "asyncio" in sys.modules:
        import asyncio
        try:
            current_task = asyncio.current_task  # type: ignore[attr-defined]
        except AttributeError:
            current_task = asyncio.Task.current_task  # type: ignore[attr-defined]
        try:
            if current_task() is not None:
                return "asyncio"
        except RuntimeError:
            pass

    # Sniff for curio (for now)
    if 'curio' in sys.modules:
        from curio.meta import curio_running
        if curio_running():
            return 'curio'

    raise AsyncLibraryNotFoundError(
        "unknown async library, or not in async context"
    )


def current_async_library() -> str | None:
    if sniffio is None:
        # If sniffio is not installed, we assume we're either running asyncio or nothing
        import asyncio

        try:
            asyncio.get_running_loop()
            return "asyncio"
        except RuntimeError:
            pass
    else:
        try:
            return sniffio.current_async_library()
        except sniffio.AsyncLibraryNotFoundError:
            pass

    return None

