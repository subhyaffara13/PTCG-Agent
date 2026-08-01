
def _flint_version_okay(flint_version):
    major, minor = flint_version.split('.')[:2]
    flint_ver = f'{major}.{minor}'
    return flint_ver in _PYTHON_FLINT_VERSION_NEEDED

