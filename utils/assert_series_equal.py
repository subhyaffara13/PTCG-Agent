
def assert_series_equal(
    left,
    right,
    check_dtype: bool | Literal["equiv"] = True,
    check_index_type: bool | Literal["equiv"] = "equiv",
    check_series_type: bool = True,
    check_names: bool = True,
    check_exact: bool | lib.NoDefault = lib.no_default,
    check_datetimelike_compat: bool = False,
    check_categorical: bool = True,
    check_category_order: bool = True,
    check_freq: bool = True,
    check_flags: bool = True,
    rtol: float | lib.NoDefault = lib.no_default,
    atol: float | lib.NoDefault = lib.no_default,
    obj: str = "Series",
    *,
    check_index: bool = True,
    check_like: bool = False,
) -> None:
    """
    Check that left and right Series are equal.

    Parameters
    ----------
    left : Series
        First Series to compare.
    right : Series
        Second Series to compare.
    check_dtype : bool, default True
        Whether to check the Series dtype is identical.
    check_index_type : bool or {'equiv'}, default 'equiv'
        Whether to check the Index class, dtype and inferred_type
        are identical.
    check_series_type : bool, default True
         Whether to check the Series class is identical.
    check_names : bool, default True
        Whether to check the Series and Index names attribute.
    check_exact : bool, default False
        Whether to compare number exactly. This also applies when checking
        Index equivalence.

        .. versionchanged:: 2.2.0

            Defaults to True for integer dtypes if none of
            ``check_exact``, ``rtol`` and ``atol`` are specified.

        .. versionchanged:: 3.0.0

            check_exact for comparing the Indexes defaults to True by
            checking if an Index is of integer dtypes.

    check_datetimelike_compat : bool, default False
        Compare datetime-like which is comparable ignoring dtype.

        .. deprecated:: 3.0

    check_categorical : bool, default True
        Whether to compare internal Categorical exactly.
    check_category_order : bool, default True
        Whether to compare category order of internal Categoricals.
    check_freq : bool, default True
        Whether to check the `freq` attribute on a DatetimeIndex or TimedeltaIndex.
    check_flags : bool, default True
        Whether to check the `flags` attribute.
    rtol : float, default 1e-5
        Relative tolerance. Only used when check_exact is False.
    atol : float, default 1e-8
        Absolute tolerance. Only used when check_exact is False.
    obj : str, default 'Series'
        Specify object name being compared, internally used to show appropriate
        assertion message.
    check_index : bool, default True
        Whether to check index equivalence. If False, then compare only values.
    check_like : bool, default False
        If True, ignore the order of the index. Must be False if check_index is False.
        Note: same labels must be with the same data.

    See Also
    --------
    testing.assert_index_equal : Check that two Indexes are equal.
    testing.assert_frame_equal : Check that two DataFrames are equal.

    Examples
    --------
    >>> from pandas import testing as tm
    >>> a = pd.Series([1, 2, 3, 4])
    >>> b = pd.Series([1, 2, 3, 4])
    >>> tm.assert_series_equal(a, b)
    """
    __tracebackhide__ = True
    if (
        check_exact is lib.no_default
        and rtol is lib.no_default
        and atol is lib.no_default
    ):
        check_exact = (
            is_numeric_dtype(left.dtype) and not is_float_dtype(left.dtype)
        ) or (is_numeric_dtype(right.dtype) and not is_float_dtype(right.dtype))
        left_index_dtypes = (
            [left.index.dtype] if left.index.nlevels == 1 else left.index.dtypes
        )
        right_index_dtypes = (
            [right.index.dtype] if right.index.nlevels == 1 else right.index.dtypes
        )
        check_exact_index = all(
            dtype.kind in "iu" for dtype in left_index_dtypes
        ) or all(dtype.kind in "iu" for dtype in right_index_dtypes)
    elif check_exact is lib.no_default:
        check_exact = False
        check_exact_index = False
    else:
        check_exact_index = check_exact

    rtol = rtol if rtol is not lib.no_default else 1.0e-5
    atol = atol if atol is not lib.no_default else 1.0e-8

    if not check_index and check_like:
        raise ValueError("check_like must be False if check_index is False")

    # instance validation
    _check_isinstance(left, right, Series)

    if check_series_type:
        assert_class_equal(left, right, obj=obj)

    # length comparison
    if len(left) != len(right):
        msg1 = f"{len(left)}, {left.index}"
        msg2 = f"{len(right)}, {right.index}"
        raise_assert_detail(obj, "Series length are different", msg1, msg2)

    if check_flags:
        assert left.flags == right.flags, f"{left.flags!r} != {right.flags!r}"

    if check_index:
        # GH #38183
        assert_index_equal(
            left.index,
            right.index,
            exact=check_index_type,
            check_names=check_names,
            check_exact=check_exact_index,
            check_categorical=check_categorical,
            check_order=not check_like,
            rtol=rtol,
            atol=atol,
            obj=f"{obj}.index",
        )

    if check_like:
        left = left.reindex_like(right)

    if check_freq and isinstance(left.index, (DatetimeIndex, TimedeltaIndex)):
        lidx = left.index
        ridx = right.index
        assert lidx.freq == ridx.freq, (lidx.freq, ridx.freq)

    if check_dtype:
        # We want to skip exact dtype checking when `check_categorical`
        # is False. We'll still raise if only one is a `Categorical`,
        # regardless of `check_categorical`
        if (
            isinstance(left.dtype, CategoricalDtype)
            and isinstance(right.dtype, CategoricalDtype)
            and not check_categorical
        ):
            pass
        else:
            assert_attr_equal("dtype", left, right, obj=f"Attributes of {obj}")
    if check_exact:
        left_values = left._values
        right_values = right._values
        # Only check exact if dtype is numeric
        if isinstance(left_values, ExtensionArray) and isinstance(
            right_values, ExtensionArray
        ):
            assert_extension_array_equal(
                left_values,
                right_values,
                check_dtype=check_dtype,
                index_values=left.index,
                obj=str(obj),
            )
        else:
            # convert both to NumPy if not, check_dtype would raise earlier
            lv, rv = left_values, right_values
            if isinstance(left_values, ExtensionArray):
                lv = left_values.to_numpy()
            if isinstance(right_values, ExtensionArray):
                rv = right_values.to_numpy()
            assert_numpy_array_equal(
                lv,
                rv,
                check_dtype=check_dtype,
                obj=str(obj),
                index_values=left.index,
            )
    elif check_datetimelike_compat and (
        needs_i8_conversion(left.dtype) or needs_i8_conversion(right.dtype)
    ):
        # we want to check only if we have compat dtypes
        # e.g. integer and M|m are NOT compat, but we can simply check
        # the values in that case

        # datetimelike may have different objects (e.g. datetime.datetime
        # vs Timestamp) but will compare equal
        if not Index(left._values).equals(Index(right._values)):
            msg = (
                f"[datetimelike_compat=True] {left._values} "
                f"is not equal to {right._values}."
            )
            raise AssertionError(msg)
    elif isinstance(left.dtype, IntervalDtype) and isinstance(
        right.dtype, IntervalDtype
    ):
        assert_interval_array_equal(left.array, right.array)
    elif isinstance(left.dtype, CategoricalDtype) or isinstance(
        right.dtype, CategoricalDtype
    ):
        _testing.assert_almost_equal(
            left._values,
            right._values,
            rtol=rtol,
            atol=atol,
            check_dtype=bool(check_dtype),
            obj=str(obj),
            index_values=left.index,
        )
    elif isinstance(left.dtype, ExtensionDtype) and isinstance(
        right.dtype, ExtensionDtype
    ):
        assert_extension_array_equal(
            left._values,
            right._values,
            rtol=rtol,
            atol=atol,
            check_dtype=check_dtype,
            index_values=left.index,
            obj=str(obj),
        )
    elif is_extension_array_dtype_and_needs_i8_conversion(
        left.dtype, right.dtype
    ) or is_extension_array_dtype_and_needs_i8_conversion(right.dtype, left.dtype):
        assert_extension_array_equal(
            left._values,
            right._values,
            check_dtype=check_dtype,
            index_values=left.index,
            obj=str(obj),
        )
    elif needs_i8_conversion(left.dtype) and needs_i8_conversion(right.dtype):
        # DatetimeArray or TimedeltaArray
        assert_extension_array_equal(
            left._values,
            right._values,
            check_dtype=check_dtype,
            index_values=left.index,
            obj=str(obj),
        )
    else:
        _testing.assert_almost_equal(
            left._values,
            right._values,
            rtol=rtol,
            atol=atol,
            check_dtype=bool(check_dtype),
            obj=str(obj),
            index_values=left.index,
        )

    # metadata comparison
    if check_names:
        assert_attr_equal("name", left, right, obj=obj)

    if check_categorical:
        if isinstance(left.dtype, CategoricalDtype) or isinstance(
            right.dtype, CategoricalDtype
        ):
            assert_categorical_equal(
                left._values,
                right._values,
                obj=f"{obj} category",
                check_category_order=check_category_order,
            )

