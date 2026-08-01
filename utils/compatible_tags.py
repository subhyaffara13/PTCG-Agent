
def compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter compatible with the Python version
    specified by ``python_version``.

    The specific tags generated are:

    - ``py*-none-<platform>``
    - ``<interpreter>-none-any`` if ``interpreter`` is provided
    - ``py*-none-any``

    :param Sequence python_version: A one- or two-item sequence representing the
                                 compatible version of Python. Defaults to
                                 ``sys.version_info[:2]``.
    :param str interpreter: The name of the interpreter (if known), e.g.
                            ``"cp38"``. Defaults to the current interpreter.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    """
    if not python_version:
        python_version = sys.version_info[:2]
    platforms = list(platforms or platform_tags())
    for version in _py_interpreter_range(python_version):
        for platform_ in platforms:
            yield Tag(version, "none", platform_)
    if interpreter:
        yield Tag(interpreter, "none", "any")
    for version in _py_interpreter_range(python_version):
        yield Tag(version, "none", "any")


def compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
) -> Iterator[Tag]:
    """
    Yields the sequence of tags that are compatible with a specific version of Python.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any  # ... if `interpreter` is provided.
    - py*-none-any
    """
    if not python_version:
        python_version = sys.version_info[:2]
    platforms = list(platforms or platform_tags())
    for version in _py_interpreter_range(python_version):
        for platform_ in platforms:
            yield Tag(version, "none", platform_)
    if interpreter:
        yield Tag(interpreter, "none", "any")
    for version in _py_interpreter_range(python_version):
        yield Tag(version, "none", "any")


def compatible_tags(
    python_version: Optional[PythonVersion] = None,
    interpreter: Optional[str] = None,
    platforms: Optional[Iterable[str]] = None,
) -> Iterator[Tag]:
    """
    Yields the sequence of tags that are compatible with a specific version of Python.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any  # ... if `interpreter` is provided.
    - py*-none-any
    """
    if not python_version:
        python_version = sys.version_info[:2]
    platforms = list(platforms or _platform_tags())
    for version in _py_interpreter_range(python_version):
        for platform_ in platforms:
            yield Tag(version, "none", platform_)
    if interpreter:
        yield Tag(interpreter, "none", "any")
    for version in _py_interpreter_range(python_version):
        yield Tag(version, "none", "any")


def compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter compatible with the Python version
    specified by ``python_version``.

    The specific tags generated are:

    - ``py*-none-<platform>``
    - ``<interpreter>-none-any`` if ``interpreter`` is provided
    - ``py*-none-any``

    :param Sequence python_version: A one- or two-item sequence representing the
                                 compatible version of Python. Defaults to
                                 ``sys.version_info[:2]``.
    :param str interpreter: The name of the interpreter (if known), e.g.
                            ``"cp38"``. Defaults to the current interpreter.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    """
    if not python_version:
        python_version = sys.version_info[:2]
    platforms = list(platforms or platform_tags())
    for version in _py_interpreter_range(python_version):
        for platform_ in platforms:
            yield Tag(version, "none", platform_)
    if interpreter:
        yield Tag(interpreter, "none", "any")
    for version in _py_interpreter_range(python_version):
        yield Tag(version, "none", "any")

