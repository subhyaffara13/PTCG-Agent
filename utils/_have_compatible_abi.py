
def _have_compatible_abi(executable: str, archs: Sequence[str]) -> bool:
    if "armv7l" in archs:
        return _is_linux_armhf(executable)
    if "i686" in archs:
        return _is_linux_i686(executable)
    return any(arch in _ALLOWED_ARCHS for arch in archs)


def _have_compatible_abi(executable: str, archs: Sequence[str]) -> bool:
    if "armv7l" in archs:
        return _is_linux_armhf(executable)
    if "i686" in archs:
        return _is_linux_i686(executable)
    return any(arch in _ALLOWED_ARCHS for arch in archs)


def _have_compatible_abi(arch: str) -> bool:
    if arch == "armv7l":
        return _is_linux_armhf()
    if arch == "i686":
        return _is_linux_i686()
    return arch in {"x86_64", "aarch64", "ppc64", "ppc64le", "s390x"}


def _have_compatible_abi(executable: str, archs: Sequence[str]) -> bool:
    if "armv7l" in archs:
        return _is_linux_armhf(executable)
    if "i686" in archs:
        return _is_linux_i686(executable)
    return any(arch in _ALLOWED_ARCHS for arch in archs)

