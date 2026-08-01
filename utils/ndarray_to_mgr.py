
def ndarray_to_mgr(
    values, index, columns, dtype: DtypeObj | None, copy: bool
) -> Manager:
    # used in DataFrame.__init__
    # input must be an ndarray, list, Series, Index, ExtensionArray
    infer_object = not isinstance(values, (ABCSeries, Index, ExtensionArray))

    if isinstance(values, ABCSeries):
        if columns is None:
            if values.name is not None:
                columns = Index([values.name])
        if index is None:
            index = values.index
        else:
            values = values.reindex(index)

        # zero len case (GH #2234)
        if not len(values) and columns is not None and len(columns):
            values = np.empty((0, 1), dtype=object)

    vdtype = getattr(values, "dtype", None)
    refs = None
    if is_1d_only_ea_dtype(vdtype) or is_1d_only_ea_dtype(dtype):
        # GH#19157

        if isinstance(values, (np.ndarray, ExtensionArray)) and values.ndim > 1:
            # GH#12513 an EA dtype passed with a 2D array, split into
            #  multiple EAs that view the values
            # error: No overload variant of "__getitem__" of "ExtensionArray"
            # matches argument type "Tuple[slice, int]"
            values = [
                values[:, n]  # type: ignore[call-overload]
                for n in range(values.shape[1])
            ]
        else:
            values = [values]

        # Handle copy semantics: already copy 1d-only EA. Other arrays will
        # be copied when consolidating the blocks
        if copy:
            values = [
                (x.copy(deep=True) if isinstance(x, Index) else x.copy())
                if isinstance(x, (ExtensionArray, Index, ABCSeries))
                and is_1d_only_ea_dtype(x.dtype)
                else x
                for x in values
            ]

        if columns is None:
            columns = Index(range(len(values)))
        else:
            columns = ensure_index(columns)

        return arrays_to_mgr(values, columns, index, dtype=dtype, consolidate=copy)

    if isinstance(values, (ABCSeries, Index)):
        if not copy and (dtype is None or astype_is_view(values.dtype, dtype)):
            refs = values._references

    if isinstance(vdtype, ExtensionDtype):
        # i.e. Datetime64TZ, PeriodDtype; cases with is_1d_only_ea_dtype(vdtype)
        #  are already caught above
        values = extract_array(values, extract_numpy=True)
        if copy:
            values = values.copy()
        if values.ndim == 1:
            values = values.reshape(-1, 1)

    elif isinstance(values, (ABCSeries, Index)):
        if copy:
            values = values._values.copy()
        else:
            values = values._values

        values = _ensure_2d(values)

    elif isinstance(values, (np.ndarray, ExtensionArray)):
        # drop subclass info
        if copy and (dtype is None or astype_is_view(values.dtype, dtype)):
            # only force a copy now if copy=True was requested
            # and a subsequent `astype` will not already result in a copy
            values = np.array(values, copy=True, order="F")
        else:
            values = np.asarray(values)
        values = _ensure_2d(values)

    else:
        # by definition an array here
        # the dtypes will be coerced to a single dtype
        values = _prep_ndarraylike(values, copy=copy)

    if dtype is not None and values.dtype != dtype:
        # GH#40110 see similar check inside sanitize_array
        values = sanitize_array(
            values,
            None,
            dtype=dtype,
            copy=copy,
            allow_2d=True,
        )

    # _prep_ndarraylike ensures that values.ndim == 2 at this point
    index, columns = _get_axes(
        values.shape[0], values.shape[1], index=index, columns=columns
    )

    _check_values_indices_shape_match(values, index, columns)

    values = values.T

    # if we don't have a dtype specified, then try to convert objects
    # on the entire block; this is to convert if we have datetimelike's
    # embedded in an object type
    if dtype is None and infer_object and is_object_dtype(values.dtype):
        obj_columns = list(values)
        maybe_datetime = [
            lib.maybe_convert_objects(
                x,
                # Here we do not convert numeric dtypes, as if we wanted that,
                #  numpy would have done it for us.
                convert_numeric=False,
                convert_non_numeric=True,
                convert_to_nullable_dtype=False,
                dtype_if_all_nat=np.dtype("M8[s]"),
            )
            for x in obj_columns
        ]
        # don't convert (and copy) the objects if no type inference occurs
        if any(x is not y for x, y in zip(obj_columns, maybe_datetime, strict=True)):
            block_values = [
                new_block_2d(ensure_block_shape(dval, 2), placement=BlockPlacement(n))
                for n, dval in enumerate(maybe_datetime)
            ]
        else:
            bp = BlockPlacement(slice(len(columns)))
            nb = new_block_2d(values, placement=bp, refs=refs)
            block_values = [nb]
    elif dtype is None and values.dtype.kind == "U" and using_string_dtype():
        dtype = StringDtype(na_value=np.nan)

        obj_columns = list(values)
        block_values = [
            new_block(
                dtype.construct_array_type()._from_sequence(data, dtype=dtype),
                BlockPlacement(slice(i, i + 1)),
                ndim=2,
            )
            for i, data in enumerate(obj_columns)
        ]

    else:
        bp = BlockPlacement(slice(len(columns)))
        nb = new_block_2d(values, placement=bp, refs=refs)
        block_values = [nb]

    if len(columns) == 0:
        # TODO: check len(values) == 0?
        block_values = []

    return create_block_manager_from_blocks(
        block_values, [columns, index], verify_integrity=False
    )

