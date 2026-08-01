
def _setuptools_commands() -> set[str]:
    try:
        # Use older API for importlib.metadata compatibility
        entry_points = metadata.distribution('setuptools').entry_points
        eps: Iterable[str] = (ep.name for ep in entry_points)
    except metadata.PackageNotFoundError:
        # during bootstrapping, distribution doesn't exist
        eps = []
    return {*distutils.command.__all__, *eps}

