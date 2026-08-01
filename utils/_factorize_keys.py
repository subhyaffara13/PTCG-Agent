
def _factorize_keys(
    lk: ArrayLike,
    rk: ArrayLike,
    sort: bool = True,
    how: str | None = None,
) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp], int]:
    """
    Encode left and right keys as enumerated types.

    This is used to get the join indexers to be used when merging DataFrames.

    Parameters
    ----------
    lk : ndarray, ExtensionArray
        Left key.
    rk : ndarray, ExtensionArray
        Right key.
    sort : bool, defaults to True
        If True, the encoding is done such that the unique elements in the
        keys are sorted.
    how: str, optional
        Used to determine if we can use hash-join. If not given, then just factorize
        keys.

    Returns
    -------
    np.ndarray[np.intp]
        Left (resp. right if called with `key='right'`) labels, as enumerated type.
    np.ndarray[np.intp]
        Right (resp. left if called with `key='right'`) labels, as enumerated type.
    int
        Number of unique elements in union of left and right labels. -1 if we used
        a hash-join.

    See Also
    --------
    merge : Merge DataFrame or named Series objects
        with a database-style join.
    algorithms.factorize : Encode the object as an enumerated type
        or categorical variable.

    Examples
    --------
    >>> lk = np.array(["a", "c", "b"])
    >>> rk = np.array(["a", "c"])

    Here, the unique values are `'a', 'b', 'c'`. With the default
    `sort=True`, the encoding will be `{0: 'a', 1: 'b', 2: 'c'}`:

    >>> pd.core.reshape.merge._factorize_keys(lk, rk)
    (array([0, 2, 1]), array([0, 2]), 3)

    With the `sort=False`, the encoding will correspond to the order
    in which the unique elements first appear: `{0: 'a', 1: 'c', 2: 'b'}`:

    >>> pd.core.reshape.merge._factorize_keys(lk, rk, sort=False)
    (array([0, 1, 2]), array([0, 1]), 3)
    """
    # TODO: if either is a RangeIndex, we can likely factorize more efficiently?

    if (
        isinstance(lk.dtype, DatetimeTZDtype) and isinstance(rk.dtype, DatetimeTZDtype)
    ) or (lib.is_np_dtype(lk.dtype, "M") and lib.is_np_dtype(rk.dtype, "M")):
        # Extract the ndarray (UTC-localized) values
        # Note: we dont need the dtypes to match, as these can still be compared
        lk, rk = cast("DatetimeArray", lk)._ensure_matching_resos(rk)
        lk = cast("DatetimeArray", lk)._ndarray
        rk = cast("DatetimeArray", rk)._ndarray

    elif (
        isinstance(lk.dtype, CategoricalDtype)
        and isinstance(rk.dtype, CategoricalDtype)
        and lk.dtype == rk.dtype
    ):
        assert isinstance(lk, Categorical)
        assert isinstance(rk, Categorical)
        # Cast rk to encoding so we can compare codes with lk

        rk = lk._encode_with_my_categories(rk)

        lk = ensure_int64(lk.codes)
        rk = ensure_int64(rk.codes)

    elif isinstance(lk, ExtensionArray) and lk.dtype == rk.dtype:
        if isinstance(lk.dtype, ArrowDtype) or (
            isinstance(lk.dtype, StringDtype) and lk.dtype.storage == "pyarrow"
        ):
            import pyarrow as pa

            from pandas.compat.pyarrow import _safe_fill_null

            len_lk = len(lk)
            lk = lk._pa_array  # type: ignore[attr-defined]
            rk = rk._pa_array  # type: ignore[union-attr]
            dc = (
                pa.chunked_array(lk.chunks + rk.chunks)  # type: ignore[union-attr]
                .combine_chunks()
                .dictionary_encode()
            )

            llab, rlab, count = (
                _safe_fill_null(dc.indices[slice(len_lk)], -1)
                .to_numpy()
                .astype(np.intp, copy=False),
                _safe_fill_null(dc.indices[slice(len_lk, None)], -1)
                .to_numpy()
                .astype(np.intp, copy=False),
                len(dc.dictionary),
            )

            if sort:
                uniques = dc.dictionary.to_numpy(zero_copy_only=False)
                llab, rlab = _sort_labels(uniques, llab, rlab)

            if dc.null_count > 0:
                lmask = llab == -1
                lany = lmask.any()
                rmask = rlab == -1
                rany = rmask.any()
                if lany:
                    np.putmask(llab, lmask, count)
                if rany:
                    np.putmask(rlab, rmask, count)
                count += 1
            return llab, rlab, count

        if not isinstance(lk, BaseMaskedArray) and not (
            # exclude arrow dtypes that would get cast to object
            isinstance(lk.dtype, ArrowDtype)
            and (
                is_numeric_dtype(lk.dtype.numpy_dtype)
                or (is_string_dtype(lk.dtype) and not sort)
            )
        ):
            lk, _ = lk._values_for_factorize()

            # error: Item "ndarray" of "Union[Any, ndarray]" has no attribute
            # "_values_for_factorize"
            rk, _ = rk._values_for_factorize()  # type: ignore[union-attr]

    if needs_i8_conversion(lk.dtype) and lk.dtype == rk.dtype:
        # GH#23917 TODO: Needs tests for non-matching dtypes
        # GH#23917 TODO: needs tests for case where lk is integer-dtype
        #  and rk is datetime-dtype
        lk = np.asarray(lk, dtype=np.int64)
        rk = np.asarray(rk, dtype=np.int64)

    klass, lk, rk = _convert_arrays_and_get_rizer_klass(lk, rk)

    rizer = klass(
        max(len(lk), len(rk)),
        uses_mask=isinstance(rk, (BaseMaskedArray, ArrowExtensionArray)),
    )

    if isinstance(lk, BaseMaskedArray):
        assert isinstance(rk, BaseMaskedArray)
        lk_data, lk_mask = lk._data, lk._mask
        rk_data, rk_mask = rk._data, rk._mask
    elif isinstance(lk, ArrowExtensionArray):
        assert isinstance(rk, ArrowExtensionArray)
        # we can only get here with numeric dtypes
        # TODO: Remove when we have a Factorizer for Arrow
        lk_data = lk.to_numpy(na_value=1, dtype=lk.dtype.numpy_dtype)
        rk_data = rk.to_numpy(na_value=1, dtype=lk.dtype.numpy_dtype)
        lk_mask, rk_mask = lk.isna(), rk.isna()
    else:
        # Argument 1 to "factorize" of "ObjectFactorizer" has incompatible type
        # "Union[ndarray[Any, dtype[signedinteger[_64Bit]]],
        # ndarray[Any, dtype[object_]]]"; expected "ndarray[Any, dtype[object_]]"
        lk_data, rk_data = lk, rk  # type: ignore[assignment]
        lk_mask, rk_mask = None, None

    hash_join_available = how == "inner" and not sort and lk.dtype.kind in "iufb"
    if hash_join_available:
        rlab = rizer.factorize(rk_data, mask=rk_mask)
        if rizer.get_count() == len(rlab):
            ridx, lidx = rizer.hash_inner_join(lk_data, lk_mask)
            return lidx, ridx, -1
        else:
            llab = rizer.factorize(lk_data, mask=lk_mask)
    else:
        llab = rizer.factorize(lk_data, mask=lk_mask)
        rlab = rizer.factorize(rk_data, mask=rk_mask)

    assert llab.dtype == np.dtype(np.intp), llab.dtype
    assert rlab.dtype == np.dtype(np.intp), rlab.dtype

    count = rizer.get_count()

    if sort:
        uniques = rizer.uniques.to_array()
        llab, rlab = _sort_labels(uniques, llab, rlab)

    # NA group
    lmask = llab == -1
    lany = lmask.any()
    rmask = rlab == -1
    rany = rmask.any()

    if lany or rany:
        if lany:
            np.putmask(llab, lmask, count)
        if rany:
            np.putmask(rlab, rmask, count)
        count += 1

    return llab, rlab, count

