
def _load_ep(ep: metadata.EntryPoint) -> tuple[str, type] | None:
    if ep.value.startswith("wheel.bdist_wheel"):
        # Ignore deprecated entrypoint from wheel and avoid warning pypa/wheel#631
        # TODO: remove check when `bdist_wheel` has been fully removed from pypa/wheel
        return None

    # Ignore all the errors
    try:
        return (ep.name, ep.load())
    except Exception as ex:
        msg = f"{ex.__class__.__name__} while trying to load entry-point {ep.name}"
        _logger.warning(f"{msg}: {ex}")
        return None

