
def platform_tags() -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for the running interpreter.
    """
    if platform.system() == "Darwin":
        return mac_platforms()
    elif platform.system() == "iOS":
        return ios_platforms()
    elif platform.system() == "Android":
        return android_platforms()
    elif platform.system() == "Linux":
        return _linux_platforms()
    elif platform.system() == "Emscripten":
        return _emscripten_platforms()
    else:
        return _generic_platforms()


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate manylinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be manylinux-compatible.

    :returns: An iterator of compatible manylinux tags.
    """
    if not _have_compatible_abi(sys.executable, archs):
        return
    # Oldest glibc to be supported regardless of architecture is (2, 17).
    too_old_glibc2 = _GLibCVersion(2, 16)
    if set(archs) & {"x86_64", "i686"}:
        # On x86/i686 also oldest glibc to be supported is (2, 5).
        too_old_glibc2 = _GLibCVersion(2, 4)
    current_glibc = _GLibCVersion(*_get_glibc_version())
    glibc_max_list = [current_glibc]
    # We can assume compatibility across glibc major versions.
    # https://sourceware.org/bugzilla/show_bug.cgi?id=24636
    #
    # Build a list of maximum glibc versions so that we can
    # output the canonical list of all glibc from current_glibc
    # down to too_old_glibc2, including all intermediary versions.
    for glibc_major in range(current_glibc.major - 1, 1, -1):
        glibc_minor = _LAST_GLIBC_MINOR[glibc_major]
        glibc_max_list.append(_GLibCVersion(glibc_major, glibc_minor))
    for arch in archs:
        for glibc_max in glibc_max_list:
            if glibc_max.major == too_old_glibc2.major:
                min_minor = too_old_glibc2.minor
            else:
                # For other glibc major versions oldest supported is (x, 0).
                min_minor = -1
            for glibc_minor in range(glibc_max.minor, min_minor, -1):
                glibc_version = _GLibCVersion(glibc_max.major, glibc_minor)
                if _is_compatible(arch, glibc_version):
                    yield "manylinux_{}_{}_{}".format(*glibc_version, arch)

                    # Handle the legacy manylinux1, manylinux2010, manylinux2014 tags.
                    if legacy_tag := _LEGACY_MANYLINUX_MAP.get(glibc_version):
                        yield f"{legacy_tag}_{arch}"


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate musllinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be musllinux-compatible.

    :returns: An iterator of compatible musllinux tags.
    """
    sys_musl = _get_musl_version(sys.executable)
    if sys_musl is None:  # Python not dynamically linked against musl.
        return
    for arch in archs:
        for minor in range(sys_musl.minor, -1, -1):
            yield f"musllinux_{sys_musl.major}_{minor}_{arch}"


def platform_tags() -> Iterator[str]:
    """
    Provides the platform tags for this installation.
    """
    if platform.system() == "Darwin":
        return mac_platforms()
    elif platform.system() == "iOS":
        return ios_platforms()
    elif platform.system() == "Android":
        return android_platforms()
    elif platform.system() == "Linux":
        return _linux_platforms()
    else:
        return _generic_platforms()


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate manylinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be manylinux-compatible.

    :returns: An iterator of compatible manylinux tags.
    """
    if not _have_compatible_abi(sys.executable, archs):
        return
    # Oldest glibc to be supported regardless of architecture is (2, 17).
    too_old_glibc2 = _GLibCVersion(2, 16)
    if set(archs) & {"x86_64", "i686"}:
        # On x86/i686 also oldest glibc to be supported is (2, 5).
        too_old_glibc2 = _GLibCVersion(2, 4)
    current_glibc = _GLibCVersion(*_get_glibc_version())
    glibc_max_list = [current_glibc]
    # We can assume compatibility across glibc major versions.
    # https://sourceware.org/bugzilla/show_bug.cgi?id=24636
    #
    # Build a list of maximum glibc versions so that we can
    # output the canonical list of all glibc from current_glibc
    # down to too_old_glibc2, including all intermediary versions.
    for glibc_major in range(current_glibc.major - 1, 1, -1):
        glibc_minor = _LAST_GLIBC_MINOR[glibc_major]
        glibc_max_list.append(_GLibCVersion(glibc_major, glibc_minor))
    for arch in archs:
        for glibc_max in glibc_max_list:
            if glibc_max.major == too_old_glibc2.major:
                min_minor = too_old_glibc2.minor
            else:
                # For other glibc major versions oldest supported is (x, 0).
                min_minor = -1
            for glibc_minor in range(glibc_max.minor, min_minor, -1):
                glibc_version = _GLibCVersion(glibc_max.major, glibc_minor)
                if _is_compatible(arch, glibc_version):
                    yield "manylinux_{}_{}_{}".format(*glibc_version, arch)

                    # Handle the legacy manylinux1, manylinux2010, manylinux2014 tags.
                    if legacy_tag := _LEGACY_MANYLINUX_MAP.get(glibc_version):
                        yield f"{legacy_tag}_{arch}"


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate musllinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be musllinux-compatible.

    :returns: An iterator of compatible musllinux tags.
    """
    sys_musl = _get_musl_version(sys.executable)
    if sys_musl is None:  # Python not dynamically linked against musl.
        return
    for arch in archs:
        for minor in range(sys_musl.minor, -1, -1):
            yield f"musllinux_{sys_musl.major}_{minor}_{arch}"


def platform_tags(linux: str, arch: str) -> Iterator[str]:
    if not _have_compatible_abi(arch):
        return
    # Oldest glibc to be supported regardless of architecture is (2, 17).
    too_old_glibc2 = _GLibCVersion(2, 16)
    if arch in {"x86_64", "i686"}:
        # On x86/i686 also oldest glibc to be supported is (2, 5).
        too_old_glibc2 = _GLibCVersion(2, 4)
    current_glibc = _GLibCVersion(*_get_glibc_version())
    glibc_max_list = [current_glibc]
    # We can assume compatibility across glibc major versions.
    # https://sourceware.org/bugzilla/show_bug.cgi?id=24636
    #
    # Build a list of maximum glibc versions so that we can
    # output the canonical list of all glibc from current_glibc
    # down to too_old_glibc2, including all intermediary versions.
    for glibc_major in range(current_glibc.major - 1, 1, -1):
        glibc_minor = _LAST_GLIBC_MINOR[glibc_major]
        glibc_max_list.append(_GLibCVersion(glibc_major, glibc_minor))
    for glibc_max in glibc_max_list:
        if glibc_max.major == too_old_glibc2.major:
            min_minor = too_old_glibc2.minor
        else:
            # For other glibc major versions oldest supported is (x, 0).
            min_minor = -1
        for glibc_minor in range(glibc_max.minor, min_minor, -1):
            glibc_version = _GLibCVersion(glibc_max.major, glibc_minor)
            tag = "manylinux_{}_{}".format(*glibc_version)
            if _is_compatible(tag, arch, glibc_version):
                yield linux.replace("linux", tag)
            # Handle the legacy manylinux1, manylinux2010, manylinux2014 tags.
            if glibc_version in _LEGACY_MANYLINUX_MAP:
                legacy_tag = _LEGACY_MANYLINUX_MAP[glibc_version]
                if _is_compatible(legacy_tag, arch, glibc_version):
                    yield linux.replace("linux", legacy_tag)


def platform_tags(arch: str) -> Iterator[str]:
    """Generate musllinux tags compatible to the current platform.

    :param arch: Should be the part of platform tag after the ``linux_``
        prefix, e.g. ``x86_64``. The ``linux_`` prefix is assumed as a
        prerequisite for the current platform to be musllinux-compatible.

    :returns: An iterator of compatible musllinux tags.
    """
    sys_musl = _get_musl_version(sys.executable)
    if sys_musl is None:  # Python not dynamically linked against musl.
        return
    for minor in range(sys_musl.minor, -1, -1):
        yield f"musllinux_{sys_musl.major}_{minor}_{arch}"


def platform_tags() -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for the running interpreter.
    """
    if platform.system() == "Darwin":
        return mac_platforms()
    elif platform.system() == "iOS":
        return ios_platforms()
    elif platform.system() == "Android":
        return android_platforms()
    elif platform.system() == "Linux":
        return _linux_platforms()
    elif platform.system() == "Emscripten":
        return _emscripten_platforms()
    else:
        return _generic_platforms()


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate manylinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be manylinux-compatible.

    :returns: An iterator of compatible manylinux tags.
    """
    if not _have_compatible_abi(sys.executable, archs):
        return
    # Oldest glibc to be supported regardless of architecture is (2, 17).
    too_old_glibc2 = _GLibCVersion(2, 16)
    if set(archs) & {"x86_64", "i686"}:
        # On x86/i686 also oldest glibc to be supported is (2, 5).
        too_old_glibc2 = _GLibCVersion(2, 4)
    current_glibc = _GLibCVersion(*_get_glibc_version())
    glibc_max_list = [current_glibc]
    # We can assume compatibility across glibc major versions.
    # https://sourceware.org/bugzilla/show_bug.cgi?id=24636
    #
    # Build a list of maximum glibc versions so that we can
    # output the canonical list of all glibc from current_glibc
    # down to too_old_glibc2, including all intermediary versions.
    for glibc_major in range(current_glibc.major - 1, 1, -1):
        glibc_minor = _LAST_GLIBC_MINOR[glibc_major]
        glibc_max_list.append(_GLibCVersion(glibc_major, glibc_minor))
    for arch in archs:
        for glibc_max in glibc_max_list:
            if glibc_max.major == too_old_glibc2.major:
                min_minor = too_old_glibc2.minor
            else:
                # For other glibc major versions oldest supported is (x, 0).
                min_minor = -1
            for glibc_minor in range(glibc_max.minor, min_minor, -1):
                glibc_version = _GLibCVersion(glibc_max.major, glibc_minor)
                if _is_compatible(arch, glibc_version):
                    yield "manylinux_{}_{}_{}".format(*glibc_version, arch)

                    # Handle the legacy manylinux1, manylinux2010, manylinux2014 tags.
                    if legacy_tag := _LEGACY_MANYLINUX_MAP.get(glibc_version):
                        yield f"{legacy_tag}_{arch}"


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate musllinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be musllinux-compatible.

    :returns: An iterator of compatible musllinux tags.
    """
    sys_musl = _get_musl_version(sys.executable)
    if sys_musl is None:  # Python not dynamically linked against musl.
        return
    for arch in archs:
        for minor in range(sys_musl.minor, -1, -1):
            yield f"musllinux_{sys_musl.major}_{minor}_{arch}"

