
def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Yields the sequence of tag triples that the running interpreter supports.

    The iterable is ordered so that the best-matching tag is first in the
    sequence. The exact preferential order to tags is interpreter-specific, but
    in general the tag importance is in the order of:

    1. Interpreter
    2. Platform
    3. ABI

    This order is due to the fact that an ABI is inherently tied to the
    platform, but platform-specific code is not necessarily tied to the ABI. The
    interpreter is the most important tag as it dictates basic support for any
    wheel.

    The function returns an iterable in order to allow for the possible
    short-circuiting of tag generation if the entire sequence is not necessary
    and tag calculation happens to be expensive.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.

    .. versionchanged:: 21.3
        Added the `pp3-none-any` tag (:issue:`311`).
    .. versionchanged:: 27.0
        Added the `abi3t` tag (:issue:`1099`).
    """

    interp_name = interpreter_name()
    if interp_name == "cp":
        yield from cpython_tags(warn=warn)
    else:
        yield from generic_tags()

    if interp_name == "pp":
        interp = "pp3"
    elif interp_name == "cp":
        interp = "cp" + interpreter_version(warn=warn)
    else:
        interp = None
    yield from compatible_tags(interpreter=interp)


def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    """

    interp_name = interpreter_name()
    if interp_name == "cp":
        yield from cpython_tags(warn=warn)
    else:
        yield from generic_tags()

    if interp_name == "pp":
        interp = "pp3"
    elif interp_name == "cp":
        interp = "cp" + interpreter_version(warn=warn)
    else:
        interp = None
    yield from compatible_tags(interpreter=interp)


def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    """

    interp_name = interpreter_name()
    if interp_name == "cp":
        yield from cpython_tags(warn=warn)
    else:
        yield from generic_tags()

    yield from compatible_tags()


def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Yields the sequence of tag triples that the running interpreter supports.

    The iterable is ordered so that the best-matching tag is first in the
    sequence. The exact preferential order to tags is interpreter-specific, but
    in general the tag importance is in the order of:

    1. Interpreter
    2. Platform
    3. ABI

    This order is due to the fact that an ABI is inherently tied to the
    platform, but platform-specific code is not necessarily tied to the ABI. The
    interpreter is the most important tag as it dictates basic support for any
    wheel.

    The function returns an iterable in order to allow for the possible
    short-circuiting of tag generation if the entire sequence is not necessary
    and tag calculation happens to be expensive.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.

    .. versionchanged:: 21.3
        Added the `pp3-none-any` tag (:issue:`311`).
    .. versionchanged:: 27.0
        Added the `abi3t` tag (:issue:`1099`).
    """

    interp_name = interpreter_name()
    if interp_name == "cp":
        yield from cpython_tags(warn=warn)
    else:
        yield from generic_tags()

    if interp_name == "pp":
        interp = "pp3"
    elif interp_name == "cp":
        interp = "cp" + interpreter_version(warn=warn)
    else:
        interp = None
    yield from compatible_tags(interpreter=interp)

