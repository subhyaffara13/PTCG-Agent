
def generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter which requires no specialization.

    This function should be used if one of the other interpreter-specific
    functions provided by this module is not appropriate (i.e. not calculating
    tags for a CPython interpreter).

    The specific tags generated are:

    - ``<interpreter>-<abi>-<platform>``

    The ``"none"`` ABI will be added if it was not explicitly provided.

    :param str interpreter: The name of the interpreter. Defaults to being
                            calculated.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    if not interpreter:
        interp_name = interpreter_name()
        interp_version = interpreter_version(warn=warn)
        interpreter = f"{interp_name}{interp_version}"
    abis = _generic_abi() if abis is None else list(abis)
    platforms = list(platforms or platform_tags())
    if "none" not in abis:
        abis.append("none")
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)


def generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for a generic interpreter.

    The tags consist of:
    - <interpreter>-<abi>-<platform>

    The "none" ABI will be added if it was not explicitly provided.
    """
    if not interpreter:
        interp_name = interpreter_name()
        interp_version = interpreter_version(warn=warn)
        interpreter = f"{interp_name}{interp_version}"
    abis = _generic_abi() if abis is None else list(abis)
    platforms = list(platforms or platform_tags())
    if "none" not in abis:
        abis.append("none")
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)


def generic_tags(
    interpreter: Optional[str] = None,
    abis: Optional[Iterable[str]] = None,
    platforms: Optional[Iterable[str]] = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for a generic interpreter.

    The tags consist of:
    - <interpreter>-<abi>-<platform>

    The "none" ABI will be added if it was not explicitly provided.
    """
    if not interpreter:
        interp_name = interpreter_name()
        interp_version = interpreter_version(warn=warn)
        interpreter = "".join([interp_name, interp_version])
    if abis is None:
        abis = _generic_abi()
    platforms = list(platforms or _platform_tags())
    abis = list(abis)
    if "none" not in abis:
        abis.append("none")
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)


def generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter which requires no specialization.

    This function should be used if one of the other interpreter-specific
    functions provided by this module is not appropriate (i.e. not calculating
    tags for a CPython interpreter).

    The specific tags generated are:

    - ``<interpreter>-<abi>-<platform>``

    The ``"none"`` ABI will be added if it was not explicitly provided.

    :param str interpreter: The name of the interpreter. Defaults to being
                            calculated.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    if not interpreter:
        interp_name = interpreter_name()
        interp_version = interpreter_version(warn=warn)
        interpreter = f"{interp_name}{interp_version}"
    abis = _generic_abi() if abis is None else list(abis)
    platforms = list(platforms or platform_tags())
    if "none" not in abis:
        abis.append("none")
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)

