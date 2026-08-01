
def assert_extension_array_equal(
    left,
    right,
    check_dtype: bool | Literal["equiv"] = True,
    index_values=None,
    check_exact: bool | lib.NoDefault = lib.no_default,
    rtol: float | lib.NoDefault = lib.no_default,
    atol: float | lib.NoDefault = lib.no_default,
    obj: str = "ExtensionArray",
) -> None:
    """
    Check that left and right ExtensionArrays are equal.

    This method compares two ``ExtensionArray`` instances for equality,
    including checks for missing values, the dtype of the arrays, and
    the exactness of the comparison (or tolerance when comparing floats).

    Parameters
    ----------
    left, right : ExtensionArray
        The two arrays to compare.
    check_dtype : bool, default True
        Whether to check if the ExtensionArray dtypes are identical.
    index_values : Index | numpy.ndarray, default None
        Optional index (shared by both left and right), used in output.
    check_exact : bool, default False
        Whether to compare number exactly.

        .. versionchanged:: 2.2.0

            Defaults to True for integer dtypes if none of
            ``check_exact``, ``rtol`` and ``atol`` are specified.
    rtol : float, default 1e-5
        Relative tolerance. Only used when check_exact is False.
    atol : float, default 1e-8
        Absolute tolerance. Only used when check_exact is False.
    obj : str, default 'ExtensionArray'
        Specify object name being compared, internally used to show appropriate
        assertion message.

        .. versionadded:: 2.0.0

    See Also
    --------
    testing.assert_series_equal : Check that left and right ``Series`` are equal.
    testing.assert_frame_equal : Check that left and right ``DataFrame`` are equal.
    testing.assert_index_equal : Check that left and right ``Index`` are equal.

    Notes
    -----
    Missing values are checked separately from valid values.
    A mask of missing values is computed for each and checked to match.
    The remaining all-valid values are cast to object dtype and checked.

    Examples
    --------
    >>> from pandas import testing as tm
    >>> a = pd.Series([1, 2, 3, 4])
    >>> b, c = a.array, a.array
    >>> tm.assert_extension_array_equal(b, c)
    """
    if (
        check_exact is lib.no_default
        and rtol is lib.no_default
        and atol is lib.no_default
    ):
        check_exact = (
            is_numeric_dtype(left.dtype) and not is_float_dtype(left.dtype)
        ) or (is_numeric_dtype(right.dtype) and not is_float_dtype(right.dtype))
    elif check_exact is lib.no_default:
        check_exact = False

    rtol = rtol if rtol is not lib.no_default else 1.0e-5
    atol = atol if atol is not lib.no_default else 1.0e-8

    assert isinstance(left, ExtensionArray), "left is not an ExtensionArray"
    assert isinstance(right, ExtensionArray), "right is not an ExtensionArray"
    if check_dtype:
        assert_attr_equal("dtype", left, right, obj=f"Attributes of {obj}")

    if (
        isinstance(left, DatetimeLikeArrayMixin)
        and isinstance(right, DatetimeLikeArrayMixin)
        and type(right) == type(left)
    ):
        # GH 52449
        if not check_dtype and left.dtype.kind in "mM":
            if not isinstance(left.dtype, np.dtype):
                l_unit = cast(DatetimeTZDtype, left.dtype).unit
            else:
                l_unit = np.datetime_data(left.dtype)[0]
            if not isinstance(right.dtype, np.dtype):
                r_unit = cast(DatetimeTZDtype, right.dtype).unit
            else:
                r_unit = np.datetime_data(right.dtype)[0]
            if (
                l_unit != r_unit
                and compare_mismatched_resolutions(
                    left._ndarray, right._ndarray, operator.eq
                ).all()
            ):
                return
        # Avoid slow object-dtype comparisons
        # np.asarray for case where we have an np.MaskedArray
        assert_numpy_array_equal(
            np.asarray(left.asi8),
            np.asarray(right.asi8),
            index_values=index_values,
            obj=obj,
        )
        return

    left_na = np.asarray(left.isna())
    right_na = np.asarray(right.isna())
    assert_numpy_array_equal(
        left_na, right_na, obj=f"{obj} NA mask", index_values=index_values
    )

    # Specifically for StringArrayNumpySemantics, validate here we have a valid array
    if (
        isinstance(left.dtype, StringDtype)
        and left.dtype.storage == "python"
        and left.dtype.na_value is np.nan
    ):
        assert np.all(
            [np.isnan(val) for val in left._ndarray[left_na]]  # type: ignore[attr-defined]
        ), "wrong missing value sentinels"
    if (
        isinstance(right.dtype, StringDtype)
        and right.dtype.storage == "python"
        and right.dtype.na_value is np.nan
    ):
        assert np.all(
            [np.isnan(val) for val in right._ndarray[right_na]]  # type: ignore[attr-defined]
        ), "wrong missing value sentinels"

    left_valid = left[~left_na].to_numpy(dtype=object)
    right_valid = right[~right_na].to_numpy(dtype=object)
    if check_exact:
        assert_numpy_array_equal(
            left_valid, right_valid, obj=obj, index_values=index_values
        )
    else:
        _testing.assert_almost_equal(
            left_valid,
            right_valid,
            check_dtype=bool(check_dtype),
            rtol=rtol,
            atol=atol,
            obj=obj,
            index_values=index_values,
        )

