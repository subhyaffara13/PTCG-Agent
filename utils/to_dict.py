
def to_dict(named_tuple):
    """Converts a namedtuple to a dict"""
    return dict(named_tuple._asdict())


def to_dict(
    df: DataFrame,
    orient: Literal["dict", "list", "series", "split", "tight", "index"] = ...,
    *,
    into: type[MutableMappingT] | MutableMappingT,
    index: bool = ...,
) -> MutableMappingT: ...


def to_dict(
    df: DataFrame,
    orient: Literal["records"],
    *,
    into: type[MutableMappingT] | MutableMappingT,
    index: bool = ...,
) -> list[MutableMappingT]: ...


def to_dict(
    df: DataFrame,
    orient: Literal["dict", "list", "series", "split", "tight", "index"] = ...,
    *,
    into: type[dict] = ...,
    index: bool = ...,
) -> dict: ...


def to_dict(
    df: DataFrame,
    orient: Literal["records"],
    *,
    into: type[dict] = ...,
    index: bool = ...,
) -> list[dict]: ...


def to_dict(
    df: DataFrame,
    orient: Literal[
        "dict", "list", "series", "split", "tight", "records", "index"
    ] = "dict",
    *,
    into: type[MutableMappingT] | MutableMappingT = dict,  # type: ignore[assignment]
    index: bool = True,
) -> MutableMappingT | list[MutableMappingT]:
    """
    Convert the DataFrame to a dictionary.

    The type of the key-value pairs can be customized with the parameters
    (see below).

    Parameters
    ----------
    orient : str {'dict', 'list', 'series', 'split', 'tight', 'records', 'index'}
        Determines the type of the values of the dictionary.

        - 'dict' (default) : dict like {column -> {index -> value}}
        - 'list' : dict like {column -> [values]}
        - 'series' : dict like {column -> Series(values)}
        - 'split' : dict like
          {'index' -> [index], 'columns' -> [columns], 'data' -> [values]}
        - 'tight' : dict like
          {'index' -> [index], 'columns' -> [columns], 'data' -> [values],
          'index_names' -> [index.names], 'column_names' -> [column.names]}
        - 'records' : list like
          [{column -> value}, ... , {column -> value}]
        - 'index' : dict like {index -> {column -> value}}

    into : class, default dict
        The collections.abc.MutableMapping subclass used for all Mappings
        in the return value.  Can be the actual class or an empty
        instance of the mapping type you want.  If you want a
        collections.defaultdict, you must pass it initialized.

    index : bool, default True
        Whether to include the index item (and index_names item if `orient`
        is 'tight') in the returned dictionary. Can only be ``False``
        when `orient` is 'split' or 'tight'.

        .. versionadded:: 2.0.0

    Returns
    -------
    dict, list or collections.abc.Mapping
        Return a collections.abc.MutableMapping object representing the
        DataFrame. The resulting transformation depends on the `orient` parameter.
    """
    if orient != "tight" and not df.columns.is_unique:
        warnings.warn(
            "DataFrame columns are not unique, some columns will be omitted.",
            UserWarning,
            stacklevel=find_stack_level(),
        )
    # GH16122
    # error: Call to untyped function "standardize_mapping" in typed context
    into_c = com.standardize_mapping(into)  # type: ignore[no-untyped-call]

    #  error: Incompatible types in assignment (expression has type "str",
    # variable has type "Literal['dict', 'list', 'series', 'split', 'tight',
    # 'records', 'index']")
    orient = orient.lower()  # type: ignore[assignment]

    if not index and orient not in ["split", "tight"]:
        raise ValueError(
            "'index=False' is only valid when 'orient' is 'split' or 'tight'"
        )

    if orient == "series":
        # GH46470 Return quickly if orient series to avoid creating dtype objects
        return into_c((k, v) for k, v in df.items())

    if orient == "dict":
        return into_c((k, v.to_dict(into=into)) for k, v in df.items())

    box_native_indices = [
        i
        for i, col_dtype in enumerate(df.dtypes.values)
        if col_dtype == np.dtype(object) or isinstance(col_dtype, ExtensionDtype)
    ]

    are_all_object_dtype_cols = len(box_native_indices) == len(df.dtypes)

    if orient == "list":
        object_dtype_indices_as_set: set[int] = set(box_native_indices)
        box_na_values = (
            lib.no_default
            if not isinstance(col_dtype, BaseMaskedDtype)
            else libmissing.NA
            for col_dtype in df.dtypes.values
        )
        return into_c(
            (
                k,
                list(map(maybe_box_native, v.to_numpy(na_value=box_na_value)))
                if i in object_dtype_indices_as_set
                else list(map(maybe_box_native, v.to_numpy())),
            )
            for i, (box_na_value, (k, v)) in enumerate(
                zip(box_na_values, df.items(), strict=True)
            )
        )

    elif orient == "split":
        data = list(
            create_data_for_split(df, are_all_object_dtype_cols, box_native_indices)
        )

        return into_c(
            ((("index", df.index.tolist()),) if index else ())
            + (
                ("columns", df.columns.tolist()),
                ("data", data),
            )
        )

    elif orient == "tight":
        return into_c(
            ((("index", df.index.tolist()),) if index else ())
            + (
                ("columns", df.columns.tolist()),
                (
                    "data",
                    [
                        list(map(maybe_box_native, t))
                        for t in df.itertuples(index=False, name=None)
                    ],
                ),
            )
            + ((("index_names", list(df.index.names)),) if index else ())
            + (("column_names", list(df.columns.names)),)
        )

    elif orient == "records":
        columns = df.columns.tolist()
        if are_all_object_dtype_cols:
            return [
                into_c(zip(columns, map(maybe_box_native, row), strict=True))
                for row in df.itertuples(index=False, name=None)
            ]
        else:
            data = [
                into_c(zip(columns, t, strict=True))
                for t in df.itertuples(index=False, name=None)
            ]
            if box_native_indices:
                object_dtype_indices_as_set = set(box_native_indices)
                object_dtype_cols = {
                    col
                    for i, col in enumerate(df.columns)
                    if i in object_dtype_indices_as_set
                }
                for row in data:
                    for col in object_dtype_cols:
                        row[col] = maybe_box_native(row[col])
            return data  # type: ignore[return-value]

    elif orient == "index":
        if not df.index.is_unique:
            raise ValueError("DataFrame index must be unique for orient='index'.")
        columns = df.columns.tolist()
        if are_all_object_dtype_cols:
            return into_c(
                (t[0], dict(zip(df.columns, map(maybe_box_native, t[1:]), strict=True)))
                for t in df.itertuples(name=None)
            )
        elif box_native_indices:
            object_dtype_indices_as_set = set(box_native_indices)
            return into_c(
                (
                    t[0],
                    {
                        column: maybe_box_native(v)
                        if i in object_dtype_indices_as_set
                        else v
                        for i, (column, v) in enumerate(
                            zip(columns, t[1:], strict=True)
                        )
                    },
                )
                for t in df.itertuples(name=None)
            )
        else:
            return into_c(
                (t[0], dict(zip(columns, t[1:], strict=True)))
                for t in df.itertuples(name=None)
            )

    else:
        raise ValueError(f"orient '{orient}' not understood")

