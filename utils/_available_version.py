
def _available_version(package: str) -> _packaging_version.Version | None:
    """
    Get the installed version of a package as (major, minor, patch).

    Handles pre-release suffixes like "0.7.0rc1" or "3.1.0.post1" by
    stripping non-numeric tails from each component. Returns None on
    parse failure.
    """
    try:
        version = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None

    try:
        v = _packaging_version.parse(version)
    except _packaging_version.InvalidVersion:
        return None

    return v

