import pathlib

def get_purelib() -> str:
    return get_python_lib(plat_specific=False)


def get_purelib() -> str:
    return sysconfig.get_paths()["purelib"]


def get_purelib() -> str:
    """Return the default pure-Python lib location."""
    new = _sysconfig.get_purelib()
    if _USE_SYSCONFIG:
        return new

    old = _distutils.get_purelib()
    if _looks_like_deb_system_dist_packages(old):
        return old
    if _warn_if_mismatch(pathlib.Path(old), pathlib.Path(new), key="purelib"):
        _log_context()
    return old

