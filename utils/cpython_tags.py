
def cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for the CPython interpreter.

    The specific tags generated are:

    - ``cp<python_version>-<abi>-<platform>``
    - ``cp<python_version>-<stable_abi>-<platform>``
    - ``cp<python_version>-none-<platform>``
    - ``cp<older version>-<stable_abi>-<platform>`` where "older version" is all older
      minor versions down to Python 3.2 (when ``abi3`` was introduced)

    If ``python_version`` only provides a major-only version then only
    user-provided ABIs via ``abis`` and the ``none`` ABI will be used.

    The ``stable_abi`` will be either ``abi3`` or ``abi3t`` if `abi` is a
    GIL-enabled ABI like `"cp315"` or a free-threaded ABI like `"cp315t"`,
    respectively.

    :param Sequence python_version: A one- or two-item sequence representing the
                                 targeted Python version. Defaults to
                                 ``sys.version_info[:2]``.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    if not python_version:
        python_version = sys.version_info[:2]

    interpreter = f"cp{_version_nodot(python_version[:2])}"

    if abis is None:
        abis = _cpython_abis(python_version, warn) if len(python_version) > 1 else []
    abis = list(abis)
    # 'abi3' and 'none' are explicitly handled later.
    for explicit_abi in ("abi3", "none"):
        try:
            abis.remove(explicit_abi)
        except ValueError:  # noqa: PERF203
            pass

    platforms = list(platforms or platform_tags())
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)

    threading = _is_threaded_cpython(abis)
    use_abi3 = _abi3_applies(python_version, threading)
    use_abi3t = _abi3t_applies(python_version, threading)

    if use_abi3:
        yield from (Tag(interpreter, "abi3", platform_) for platform_ in platforms)
    if use_abi3t:
        yield from (Tag(interpreter, "abi3t", platform_) for platform_ in platforms)

    yield from (Tag(interpreter, "none", platform_) for platform_ in platforms)

    if use_abi3 or use_abi3t:
        for minor_version in range(python_version[1] - 1, 1, -1):
            for platform_ in platforms:
                version = _version_nodot((python_version[0], minor_version))
                interpreter = f"cp{version}"
                if use_abi3:
                    yield Tag(interpreter, "abi3", platform_)
                if use_abi3t:
                    # Support for abi3t was introduced in Python 3.15, but in
                    # principle abi3t wheels are possible for older limited API
                    # versions, so allow things like ("cp37", "abi3t", "platform")
                    yield Tag(interpreter, "abi3t", platform_)


def cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for a CPython interpreter.

    The tags consist of:
    - cp<python_version>-<abi>-<platform>
    - cp<python_version>-abi3-<platform>
    - cp<python_version>-none-<platform>
    - cp<less than python_version>-abi3-<platform>  # Older Python versions down to 3.2.

    If python_version only specifies a major version then user-provided ABIs and
    the 'none' ABItag will be used.

    If 'abi3' or 'none' are specified in 'abis' then they will be yielded at
    their normal position and not at the beginning.
    """
    if not python_version:
        python_version = sys.version_info[:2]

    interpreter = f"cp{_version_nodot(python_version[:2])}"

    if abis is None:
        abis = _cpython_abis(python_version, warn) if len(python_version) > 1 else []
    abis = list(abis)
    # 'abi3' and 'none' are explicitly handled later.
    for explicit_abi in ("abi3", "none"):
        try:
            abis.remove(explicit_abi)
        except ValueError:  # noqa: PERF203
            pass

    platforms = list(platforms or platform_tags())
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)

    threading = _is_threaded_cpython(abis)
    use_abi3 = _abi3_applies(python_version, threading)
    if use_abi3:
        yield from (Tag(interpreter, "abi3", platform_) for platform_ in platforms)
    yield from (Tag(interpreter, "none", platform_) for platform_ in platforms)

    if use_abi3:
        for minor_version in range(python_version[1] - 1, 1, -1):
            for platform_ in platforms:
                version = _version_nodot((python_version[0], minor_version))
                interpreter = f"cp{version}"
                yield Tag(interpreter, "abi3", platform_)


def cpython_tags(
    python_version: Optional[PythonVersion] = None,
    abis: Optional[Iterable[str]] = None,
    platforms: Optional[Iterable[str]] = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for a CPython interpreter.

    The tags consist of:
    - cp<python_version>-<abi>-<platform>
    - cp<python_version>-abi3-<platform>
    - cp<python_version>-none-<platform>
    - cp<less than python_version>-abi3-<platform>  # Older Python versions down to 3.2.

    If python_version only specifies a major version then user-provided ABIs and
    the 'none' ABItag will be used.

    If 'abi3' or 'none' are specified in 'abis' then they will be yielded at
    their normal position and not at the beginning.
    """
    if not python_version:
        python_version = sys.version_info[:2]

    interpreter = "cp{}".format(_version_nodot(python_version[:2]))

    if abis is None:
        if len(python_version) > 1:
            abis = _cpython_abis(python_version, warn)
        else:
            abis = []
    abis = list(abis)
    # 'abi3' and 'none' are explicitly handled later.
    for explicit_abi in ("abi3", "none"):
        try:
            abis.remove(explicit_abi)
        except ValueError:
            pass

    platforms = list(platforms or _platform_tags())
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)
    if _abi3_applies(python_version):
        yield from (Tag(interpreter, "abi3", platform_) for platform_ in platforms)
    yield from (Tag(interpreter, "none", platform_) for platform_ in platforms)

    if _abi3_applies(python_version):
        for minor_version in range(python_version[1] - 1, 1, -1):
            for platform_ in platforms:
                interpreter = "cp{version}".format(
                    version=_version_nodot((python_version[0], minor_version))
                )
                yield Tag(interpreter, "abi3", platform_)


def cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for the CPython interpreter.

    The specific tags generated are:

    - ``cp<python_version>-<abi>-<platform>``
    - ``cp<python_version>-<stable_abi>-<platform>``
    - ``cp<python_version>-none-<platform>``
    - ``cp<older version>-<stable_abi>-<platform>`` where "older version" is all older
      minor versions down to Python 3.2 (when ``abi3`` was introduced)

    If ``python_version`` only provides a major-only version then only
    user-provided ABIs via ``abis`` and the ``none`` ABI will be used.

    The ``stable_abi`` will be either ``abi3`` or ``abi3t`` if `abi` is a
    GIL-enabled ABI like `"cp315"` or a free-threaded ABI like `"cp315t"`,
    respectively.

    :param Sequence python_version: A one- or two-item sequence representing the
                                 targeted Python version. Defaults to
                                 ``sys.version_info[:2]``.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    if not python_version:
        python_version = sys.version_info[:2]

    interpreter = f"cp{_version_nodot(python_version[:2])}"

    if abis is None:
        abis = _cpython_abis(python_version, warn) if len(python_version) > 1 else []
    abis = list(abis)
    # 'abi3' and 'none' are explicitly handled later.
    for explicit_abi in ("abi3", "none"):
        try:
            abis.remove(explicit_abi)
        except ValueError:  # noqa: PERF203
            pass

    platforms = list(platforms or platform_tags())
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)

    threading = _is_threaded_cpython(abis)
    use_abi3 = _abi3_applies(python_version, threading)
    use_abi3t = _abi3t_applies(python_version, threading)

    if use_abi3:
        yield from (Tag(interpreter, "abi3", platform_) for platform_ in platforms)
    if use_abi3t:
        yield from (Tag(interpreter, "abi3t", platform_) for platform_ in platforms)

    yield from (Tag(interpreter, "none", platform_) for platform_ in platforms)

    if use_abi3 or use_abi3t:
        for minor_version in range(python_version[1] - 1, 1, -1):
            for platform_ in platforms:
                version = _version_nodot((python_version[0], minor_version))
                interpreter = f"cp{version}"
                if use_abi3:
                    yield Tag(interpreter, "abi3", platform_)
                if use_abi3t:
                    # Support for abi3t was introduced in Python 3.15, but in
                    # principle abi3t wheels are possible for older limited API
                    # versions, so allow things like ("cp37", "abi3t", "platform")
                    yield Tag(interpreter, "abi3t", platform_)

