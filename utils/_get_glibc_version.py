import os
from typing import Tuple

def _get_glibc_version() -> _GLibCVersion:
    version_str = _glibc_version_string()
    if version_str is None:
        return _GLibCVersion(-1, -1)
    return _parse_glibc_version(version_str)


def _get_glibc_version():
    try:
        ver = os.confstr("CS_GNU_LIBC_VERSION").rsplit(" ")[1]
    except Exception:
        ver = "0.0"

    return ver


def _get_glibc_version() -> _GLibCVersion:
    version_str = _glibc_version_string()
    if version_str is None:
        return _GLibCVersion(-1, -1)
    return _parse_glibc_version(version_str)


def _get_glibc_version() -> Tuple[int, int]:
    version_str = _glibc_version_string()
    if version_str is None:
        return (-1, -1)
    return _parse_glibc_version(version_str)


def _get_glibc_version() -> _GLibCVersion:
    version_str = _glibc_version_string()
    if version_str is None:
        return _GLibCVersion(-1, -1)
    return _parse_glibc_version(version_str)


def _get_glibc_version():
    try:
        ver = os.confstr('CS_GNU_LIBC_VERSION').rsplit(' ')[1]
    except Exception:
        ver = '0.0'

    return ver

