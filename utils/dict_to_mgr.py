
def dict_to_mgr(
    data: dict,
    index,
    columns,
    *,
    dtype: DtypeObj | None = None,
    copy: bool = True,
) -> Manager:
    """
    Segregate Series based on type and coerce into matrices.
    Needs to handle a lot of exceptional cases.

    Used in DataFrame.__init__
    """
    arrays: Sequence[Any]

    if columns is not None:
        columns = ensure_index(columns)
        if dtype is not None and not isinstance(dtype, np.dtype):
            # e.g. test_dataframe_from_dict_of_series
            arrays = [dtype.na_value] * len(columns)
        else:
            arrays = [np.nan] * len(columns)
        midxs = set()
        data_keys = ensure_index(data.keys())  # type: ignore[arg-type]
        data_values = list(data.values())

        for i, column in enumerate(columns):
            try:
                idx = data_keys.get_loc(column)
            except KeyError:
                midxs.add(i)
                continue
            array = data_values[idx]
            arrays[i] = array
            if is_scalar(array) and isna(array):
                midxs.add(i)

        if index is None:
            # GH10856
            # raise ValueError if only scalars in dict
            if midxs:
                index = _extract_index(
                    [array for i, array in enumerate(arrays) if i not in midxs]
                )
            else:
                index = _extract_index(arrays)
        else:
            index = ensure_index(index)

        # no obvious "empty" int column
        if midxs and not is_integer_dtype(dtype):
            # GH#1783
            for i in midxs:
                arr = construct_1d_arraylike_from_scalar(
                    arrays[i],
                    len(index),
                    dtype if dtype is not None else np.dtype("object"),
                )
                arrays[i] = arr

    else:
        keys = maybe_sequence_to_range(list(data.keys()))
        columns = Index(keys) if keys else default_index(0)
        arrays = [com.maybe_iterable_to_list(data[k]) for k in keys]

    if copy:
        # We only need to copy arrays that will not get consolidated, i.e.
        #  only EA arrays
        arrays = [
            (
                x.copy()
                if isinstance(x, ExtensionArray)
                else (
                    x.copy(deep=True)
                    if (
                        isinstance(x, Index)
                        or (isinstance(x, ABCSeries) and is_1d_only_ea_dtype(x.dtype))
                    )
                    else x
                )
            )
            for x in arrays
        ]

    return arrays_to_mgr(arrays, columns, index, dtype=dtype, consolidate=copy)

