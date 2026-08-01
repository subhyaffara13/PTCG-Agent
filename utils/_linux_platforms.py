
def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    linux = _normalize_string(sysconfig.get_platform())
    if not linux.startswith("linux_"):
        # we should never be here, just yield the sysconfig one and return
        yield linux
        return
    if is_32bit:
        if linux == "linux_x86_64":
            linux = "linux_i686"
        elif linux == "linux_aarch64":
            linux = "linux_armv8l"
    _, arch = linux.split("_", 1)
    archs = {"armv8l": ["armv8l", "armv7l"]}.get(arch, [arch])
    yield from _manylinux.platform_tags(archs)
    yield from _musllinux.platform_tags(archs)
    for arch in archs:
        yield f"linux_{arch}"


def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    linux = _normalize_string(sysconfig.get_platform())
    if not linux.startswith("linux_"):
        # we should never be here, just yield the sysconfig one and return
        yield linux
        return
    if is_32bit:
        if linux == "linux_x86_64":
            linux = "linux_i686"
        elif linux == "linux_aarch64":
            linux = "linux_armv8l"
    _, arch = linux.split("_", 1)
    archs = {"armv8l": ["armv8l", "armv7l"]}.get(arch, [arch])
    yield from _manylinux.platform_tags(archs)
    yield from _musllinux.platform_tags(archs)
    for arch in archs:
        yield f"linux_{arch}"


def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    linux = _normalize_string(sysconfig.get_platform())
    if is_32bit:
        if linux == "linux_x86_64":
            linux = "linux_i686"
        elif linux == "linux_aarch64":
            linux = "linux_armv7l"
    _, arch = linux.split("_", 1)
    yield from _manylinux.platform_tags(linux, arch)
    yield from _musllinux.platform_tags(arch)
    yield linux


def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    linux = _normalize_string(sysconfig.get_platform())
    if not linux.startswith("linux_"):
        # we should never be here, just yield the sysconfig one and return
        yield linux
        return
    if is_32bit:
        if linux == "linux_x86_64":
            linux = "linux_i686"
        elif linux == "linux_aarch64":
            linux = "linux_armv8l"
    _, arch = linux.split("_", 1)
    archs = {"armv8l": ["armv8l", "armv7l"]}.get(arch, [arch])
    yield from _manylinux.platform_tags(archs)
    yield from _musllinux.platform_tags(archs)
    for arch in archs:
        yield f"linux_{arch}"

