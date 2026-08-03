from typing import Any, Callable

def deprecate(
    deprecated: str,
    when: int | None,
    replacement: str | None = None,
    *,
    action: str | None = None,
    plural: bool = False,
    stacklevel: int = 3,
) -> None:
    """
    Deprecations helper.

    :param deprecated: Name of thing to be deprecated.
    :param when: Pillow major version to be removed in.
    :param replacement: Name of replacement.
    :param action: Instead of "replacement", give a custom call to action
        e.g. "Upgrade to new thing".
    :param plural: if the deprecated thing is plural, needing "are" instead of "is".

    Usually of the form:

        "[deprecated] is deprecated and will be removed in Pillow [when] (yyyy-mm-dd).
        Use [replacement] instead."

    You can leave out the replacement sentence:

        "[deprecated] is deprecated and will be removed in Pillow [when] (yyyy-mm-dd)"

    Or with another call to action:

        "[deprecated] is deprecated and will be removed in Pillow [when] (yyyy-mm-dd).
        [action]."
    """

    is_ = "are" if plural else "is"

    if when is None:
        removed = "a future version"
    elif when <= int(__version__.split(".")[0]):
        msg = f"{deprecated} {is_} deprecated and should be removed."
        raise RuntimeError(msg)
    elif when == 13:
        removed = "Pillow 13 (2026-10-15)"
    elif when == 14:
        removed = "Pillow 14 (2027-10-15)"
    else:
        msg = f"Unknown removal version: {when}. Update {__name__}?"
        raise ValueError(msg)

    if replacement and action:
        msg = "Use only one of 'replacement' and 'action'"
        raise ValueError(msg)

    if replacement:
        action = f". Use {replacement} instead."
    elif action:
        action = f". {action.rstrip('.')}."
    else:
        action = ""

    warnings.warn(
        f"{deprecated} {is_} deprecated and will be removed in {removed}{action}",
        DeprecationWarning,
        stacklevel=stacklevel,
    )


def deprecate(
    klass: type[Warning],
    name: str,
    alternative: Callable[..., Any],
    version: str,
    alt_name: str | None = None,
    stacklevel: int = 2,
    msg: str | None = None,
) -> Callable[[F], F]:
    """
    Return a new function that emits a deprecation warning on use.

    To use this method for a deprecated function, another function
    `alternative` with the same signature must exist. The deprecated
    function will emit a deprecation warning, and in the docstring
    it will contain the deprecation directive with the provided version
    so it can be detected for future removal.

    Parameters
    ----------
    klass : Warning
        The warning class to use.
    name : str
        Name of function to deprecate.
    alternative : func
        Function to use instead.
    version : str
        Version of pandas in which the method has been deprecated.
    alt_name : str, optional
        Name to use in preference of alternative.__name__.
    stacklevel : int, default 2
    msg : str
        The message to display in the warning.
        Default is '{name} is deprecated. Use {alt_name} instead.'
    """
    alt_name = alt_name or alternative.__name__
    warning_msg = msg or f"{name} is deprecated, use {alt_name} instead."

    @wraps(alternative)
    def wrapper(*args, **kwargs) -> Callable[..., Any]:
        warnings.warn(warning_msg, klass, stacklevel=stacklevel)
        return alternative(*args, **kwargs)

    # adding deprecated directive to the docstring
    msg = msg or f"Use `{alt_name}` instead."
    doc_error_msg = (
        "deprecate needs a correctly formatted docstring in "
        "the target function (should have a one liner short "
        "summary, and opening quotes should be in their own "
        f"line). Found:\n{alternative.__doc__}"
    )

    # when python is running in optimized mode (i.e. `-OO`), docstrings are
    # removed, so we check that a docstring with correct formatting is used
    # but we allow empty docstrings
    if alternative.__doc__:
        if alternative.__doc__.count("\n") < 3:
            raise AssertionError(doc_error_msg)
        empty1, summary, empty2, doc_string = alternative.__doc__.split("\n", 3)
        if empty1 or (empty2 and not summary):
            raise AssertionError(doc_error_msg)
        wrapper.__doc__ = dedent(
            f"""
        {summary.strip()}

        .. deprecated:: {version}
            {msg}

        {dedent(doc_string)}"""
        )
    # error: Incompatible return value type (got "Callable[[VarArg(Any), KwArg(Any)],
    # Callable[...,Any]]", expected "Callable[[F], F]")
    return wrapper  # type: ignore[return-value]

