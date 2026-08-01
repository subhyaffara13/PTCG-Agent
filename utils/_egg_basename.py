
def _egg_basename(egg_name, egg_version, py_version=None, platform=None):
    """Compute filename of the output egg. Private API."""
    name = _normalization.filename_component(egg_name)
    version = _normalization.filename_component(egg_version)
    egg = f"{name}-{version}-py{py_version or PY_MAJOR}"
    if platform:
        egg += f"-{platform}"
    return egg

