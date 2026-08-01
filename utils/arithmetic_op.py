
def arithmetic_op(left: ArrayLike, right: Any, op):
    """
    Evaluate an arithmetic operation `+`, `-`, `*`, `/`, `//`, `%`, `**`, ...

    Note: the caller is responsible for ensuring that numpy warnings are
    suppressed (with np.errstate(all="ignore")) if needed.

    Parameters
    ----------
    left : np.ndarray or ExtensionArray
    right : object
        Cannot be a DataFrame or Index.  Series is *not* excluded.
    op : {operator.add, operator.sub, ...}
        Or one of the reversed variants from roperator.

    Returns
    -------
    ndarray or ExtensionArray
        Or a 2-tuple of these in the case of divmod or rdivmod.
    """
    # NB: We assume that extract_array and ensure_wrapped_if_datetimelike
    #  have already been called on `left` and `right`,
    #  and `maybe_prepare_scalar_for_op` has already been called on `right`
    # We need to special-case datetime64/timedelta64 dtypes (e.g. because numpy
    # casts integer dtypes to timedelta64 when operating with timedelta64 - GH#22390)
    if isinstance(right, list):
        # GH#62423
        right = sanitize_array(right, None)
    right = ensure_wrapped_if_datetimelike(right)

    if (
        should_extension_dispatch(left, right)
        or isinstance(right, (Timedelta, BaseOffset, Timestamp))
        or right is NaT
    ):
        # Timedelta/Timestamp and other custom scalars are included in the check
        # because numexpr will fail on it, see GH#31457
        res_values = op(left, right)
    else:
        # TODO we should handle EAs consistently and move this check before the if/else
        # (https://github.com/pandas-dev/pandas/issues/41165)
        # error: Argument 2 to "_bool_arith_check" has incompatible type
        # "Union[ExtensionArray, ndarray[Any, Any]]"; expected "ndarray[Any, Any]"
        _bool_arith_check(op, left, right)  # type: ignore[arg-type]

        # error: Argument 1 to "_na_arithmetic_op" has incompatible type
        # "Union[ExtensionArray, ndarray[Any, Any]]"; expected "ndarray[Any, Any]"
        res_values = _na_arithmetic_op(left, right, op)  # type: ignore[arg-type]

    return res_values

