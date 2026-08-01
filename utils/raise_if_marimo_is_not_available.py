
def raise_if_marimo_is_not_available(min_version=MARIMO_MIN_VERSION, max_version=None):
    """Raise with an informative error message if Marimo is not available"""
    version = marimo_version()
    if version == "N/A":
        raise MarimoError(f"The Marimo format requires 'marimo>={min_version}', but marimo was not found")

    if parse(version) < parse(min_version):
        raise MarimoError(f"The Marimo format requires 'marimo>={min_version}', but marimo=={version} was found")

    if max_version and parse(version) > parse(max_version):
        raise MarimoError(f"The Marimo format requires 'marimo<={max_version}', but marimo=={version} was found")

    return version

