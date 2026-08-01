
def _get_backend_mod() -> type[matplotlib.backend_bases._Backend]:
    """
    Ensure that a backend is selected and return it.

    This is currently private, but may be made public in the future.
    """
    if _backend_mod is None:
        # Use rcParams._get("backend") to avoid going through the fallback
        # logic (which will (re)import pyplot and then call switch_backend if
        # we need to resolve the auto sentinel)
        switch_backend(rcParams._get("backend"))
    return cast(type[matplotlib.backend_bases._Backend], _backend_mod)

