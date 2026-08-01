
def _refine_defaults_read(
    dialect: str | csv.Dialect | None,
    delimiter: str | None | lib.NoDefault,
    engine: CSVEngine | None,
    sep: str | None | lib.NoDefault,
    on_bad_lines: str | Callable,
    names: Sequence[Hashable] | None | lib.NoDefault,
    defaults: dict[str, Any],
    dtype_backend: DtypeBackend | lib.NoDefault,
):
    """Validate/refine default values of input parameters of read_csv, read_table.

    Parameters
    ----------
    dialect : str or csv.Dialect
        If provided, this parameter will override values (default or not) for the
        following parameters: `delimiter`, `doublequote`, `escapechar`,
        `skipinitialspace`, `quotechar`, and `quoting`. If it is necessary to
        override values, a ParserWarning will be issued. See csv.Dialect
        documentation for more details.
    delimiter : str or object
        Alias for sep.
    engine : {'c', 'python'}
        Parser engine to use. The C engine is faster while the python engine is
        currently more feature-complete.
    sep : str or object
        A delimiter provided by the user (str) or a sentinel value, i.e.
        pandas._libs.lib.no_default.
    on_bad_lines : str, callable
        An option for handling bad lines or a sentinel value(None).
    names : array-like, optional
        List of column names to use. If the file contains a header row,
        then you should explicitly pass ``header=0`` to override the column names.
        Duplicates in this list are not allowed.
    defaults: dict
        Default values of input parameters.

    Returns
    -------
    kwds : dict
        Input parameters with correct values.
    """
    # fix types for sep, delimiter to Union(str, Any)
    delim_default = defaults["delimiter"]
    kwds: dict[str, Any] = {}
    # gh-23761
    #
    # When a dialect is passed, it overrides any of the overlapping
    # parameters passed in directly. We don't want to warn if the
    # default parameters were passed in (since it probably means
    # that the user didn't pass them in explicitly in the first place).
    #
    # "delimiter" is the annoying corner case because we alias it to
    # "sep" before doing comparison to the dialect values later on.
    # Thus, we need a flag to indicate that we need to "override"
    # the comparison to dialect values by checking if default values
    # for BOTH "delimiter" and "sep" were provided.
    if dialect is not None:
        kwds["sep_override"] = delimiter is None and (
            sep is lib.no_default or sep == delim_default
        )

    if delimiter and (sep is not lib.no_default):
        raise ValueError("Specified a sep and a delimiter; you can only specify one.")

    kwds["names"] = None if names is lib.no_default else names

    # Alias sep -> delimiter.
    if delimiter is None:
        delimiter = sep

    if delimiter == "\n":
        raise ValueError(
            r"Specified \n as separator or delimiter. This forces the python engine "
            "which does not accept a line terminator. Hence it is not allowed to use "
            "the line terminator as separator.",
        )

    if delimiter is lib.no_default:
        # assign default separator value
        kwds["delimiter"] = delim_default
    else:
        kwds["delimiter"] = delimiter

    if engine is not None:
        kwds["engine_specified"] = True
    else:
        kwds["engine"] = "c"
        kwds["engine_specified"] = False

    if on_bad_lines == "error":
        kwds["on_bad_lines"] = ParserBase.BadLineHandleMethod.ERROR
    elif on_bad_lines == "warn":
        kwds["on_bad_lines"] = ParserBase.BadLineHandleMethod.WARN
    elif on_bad_lines == "skip":
        kwds["on_bad_lines"] = ParserBase.BadLineHandleMethod.SKIP
    elif callable(on_bad_lines):
        if engine not in ["python", "pyarrow"]:
            raise ValueError(
                "on_bad_line can only be a callable function "
                "if engine='python' or 'pyarrow'"
            )
        kwds["on_bad_lines"] = on_bad_lines
    else:
        raise ValueError(f"Argument {on_bad_lines} is invalid for on_bad_lines")

    check_dtype_backend(dtype_backend)

    kwds["dtype_backend"] = dtype_backend

    return kwds

