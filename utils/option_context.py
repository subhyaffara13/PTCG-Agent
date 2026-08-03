from typing import Any

def option_context(*args) -> Generator[None]:
    """
    Context manager to temporarily set options in a ``with`` statement.

    This method allows users to set one or more pandas options temporarily
    within a controlled block. The previous options' values are restored
    once the block is exited. This is useful when making temporary adjustments
    to pandas' behavior without affecting the global state.

    Parameters
    ----------
    *args : str | object | dict
        An even amount of arguments provided in pairs which will be
        interpreted as (pattern, value) pairs. Alternatively, a single
        dictionary of {pattern: value} may be provided.

    Returns
    -------
    None
        No return value.

    Yields
    ------
    None
        No yield value.

    See Also
    --------
    get_option : Retrieve the value of the specified option.
    set_option : Set the value of the specified option.
    reset_option : Reset one or more options to their default value.
    describe_option : Print the description for one or more registered options.

    Notes
    -----
    For all available options, please view the :ref:`User Guide <options.available>`
    or use ``pandas.describe_option()``.

    Examples
    --------
    >>> from pandas import option_context
    >>> with option_context("display.max_rows", 10, "display.max_columns", 5):
    ...     pass
    >>> with option_context({"display.max_rows": 10, "display.max_columns": 5}):
    ...     pass
    """
    if len(args) == 1 and isinstance(args[0], dict):
        args = tuple(kv for item in args[0].items() for kv in item)

    if len(args) % 2 != 0 or len(args) < 2:
        raise ValueError(
            "Provide an even amount of arguments as "
            "option_context(pat, val, pat, val...)."
        )

    ops = tuple(zip(args[::2], args[1::2], strict=True))
    undo: tuple[tuple[Any, Any], ...] = ()
    try:
        undo = tuple((pat, get_option(pat)) for pat, val in ops)
        for pat, val in ops:
            set_option(pat, val)
        yield
    finally:
        for pat, val in undo:
            set_option(pat, val)

