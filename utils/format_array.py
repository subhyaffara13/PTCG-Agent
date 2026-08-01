
def format_array(
    values: ArrayLike,
    formatter: Callable | None,
    float_format: FloatFormatType | None = None,
    na_rep: str = "NaN",
    digits: int | None = None,
    space: str | int | None = None,
    justify: str = "right",
    decimal: str = ".",
    leading_space: bool | None = True,
    quoting: int | None = None,
    fallback_formatter: Callable | None = None,
) -> list[str]:
    """
    Format an array for printing.

    Parameters
    ----------
    values : np.ndarray or ExtensionArray
    formatter
    float_format
    na_rep
    digits
    space
    justify
    decimal
    leading_space : bool, optional, default True
        Whether the array should be formatted with a leading space.
        When an array as a column of a Series or DataFrame, we do want
        the leading space to pad between columns.

        When formatting an Index subclass
        (e.g. IntervalIndex._get_values_for_csv), we don't want the
        leading space since it should be left-aligned.
    fallback_formatter

    Returns
    -------
    List[str]
    """
    fmt_klass: type[_GenericArrayFormatter]
    if lib.is_np_dtype(values.dtype, "M"):
        fmt_klass = _Datetime64Formatter
        values = cast(DatetimeArray, values)
    elif isinstance(values.dtype, DatetimeTZDtype):
        fmt_klass = _Datetime64TZFormatter
        values = cast(DatetimeArray, values)
    elif lib.is_np_dtype(values.dtype, "m"):
        fmt_klass = _Timedelta64Formatter
        values = cast(TimedeltaArray, values)
    elif isinstance(values.dtype, ExtensionDtype):
        fmt_klass = _ExtensionArrayFormatter
    elif lib.is_np_dtype(values.dtype, "fc"):
        fmt_klass = FloatArrayFormatter
    elif lib.is_np_dtype(values.dtype, "iu"):
        fmt_klass = _IntArrayFormatter
    else:
        fmt_klass = _GenericArrayFormatter

    if space is None:
        space = 12

    if float_format is None:
        float_format = get_option("display.float_format")

    if digits is None:
        digits = get_option("display.precision")

    fmt_obj = fmt_klass(
        values,
        digits=digits,
        na_rep=na_rep,
        float_format=float_format,
        formatter=formatter,
        space=space,
        justify=justify,
        decimal=decimal,
        leading_space=leading_space,
        quoting=quoting,
        fallback_formatter=fallback_formatter,
    )

    return fmt_obj.get_result()

