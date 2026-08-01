
def _maybe_wrap_formatter(
    formatter: BaseFormatter | None = None,
    na_rep: str | None = None,
    precision: int | None = None,
    decimal: str = ".",
    thousands: str | None = None,
    escape: str | None = None,
    hyperlinks: str | None = None,
) -> Callable:
    """
    Allows formatters to be expressed as str, callable or None, where None returns
    a default formatting function. wraps with na_rep, and precision where they are
    available.
    """
    # Get initial func from input string, input callable, or from default factory
    if isinstance(formatter, str):
        func_0 = lambda x: formatter.format(x)
    elif callable(formatter):
        func_0 = formatter
    elif formatter is None:
        precision = (
            get_option("styler.format.precision") if precision is None else precision
        )
        func_0 = partial(
            _default_formatter, precision=precision, thousands=(thousands is not None)
        )
    else:
        raise TypeError(f"'formatter' expected str or callable, got {type(formatter)}")

    # Replace chars if escaping
    if escape is not None:
        func_1 = lambda x: func_0(_str_escape(x, escape=escape))
    else:
        func_1 = func_0

    # Replace decimals and thousands if non-standard inputs detected
    if decimal != "." or (thousands is not None and thousands != ","):
        func_2 = _wrap_decimal_thousands(func_1, decimal=decimal, thousands=thousands)
    else:
        func_2 = func_1

    # Render links
    if hyperlinks is not None:
        func_3 = lambda x: func_2(_render_href(x, format=hyperlinks))
    else:
        func_3 = func_2

    # Replace missing values if na_rep
    if na_rep is None:
        return func_3
    else:
        return lambda x: na_rep if (isna(x) is True) else func_3(x)

