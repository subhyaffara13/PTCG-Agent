
def arrow_table_to_pandas(
    table: pyarrow.Table,
    dtype_backend: DtypeBackend | Literal["numpy"] | lib.NoDefault = lib.no_default,
    null_to_int64: bool = False,
    to_pandas_kwargs: dict | None = None,
    dtype: DtypeArg | None = None,
    names: Sequence[Hashable] | None = None,
) -> pd.DataFrame:
    pa = import_optional_dependency("pyarrow")

    to_pandas_kwargs = {} if to_pandas_kwargs is None else to_pandas_kwargs

    types_mapper: type[pd.ArrowDtype] | None | Callable
    if dtype_backend == "numpy_nullable":
        mapping = _arrow_dtype_mapping()
        if null_to_int64:
            # Modify the default mapping to also map null to Int64
            # (to match other engines - only for CSV parser)
            mapping[pa.null()] = pd.Int64Dtype()
        types_mapper = mapping.get
    elif dtype_backend == "pyarrow":
        types_mapper = pd.ArrowDtype
    elif using_string_dtype():
        if pa_version_under19p0:
            types_mapper = _arrow_string_types_mapper()
        elif dtype is not None:
            # GH#56136 Avoid lossy conversion to float64
            # We'll convert to numpy below if
            types_mapper = {
                pa.int8(): pd.Int8Dtype(),
                pa.int16(): pd.Int16Dtype(),
                pa.int32(): pd.Int32Dtype(),
                pa.int64(): pd.Int64Dtype(),
            }.get
        else:
            types_mapper = None
    elif dtype_backend is lib.no_default or dtype_backend == "numpy":
        if dtype is not None:
            # GH#56136 Avoid lossy conversion to float64
            # We'll convert to numpy below if
            types_mapper = {
                pa.int8(): pd.Int8Dtype(),
                pa.int16(): pd.Int16Dtype(),
                pa.int32(): pd.Int32Dtype(),
                pa.int64(): pd.Int64Dtype(),
            }.get
        else:
            types_mapper = None
    else:
        raise NotImplementedError

    df = table.to_pandas(types_mapper=types_mapper, **to_pandas_kwargs)
    df = _post_convert_dtypes(df, dtype_backend, dtype, names)
    df = _normalize_timezone_dtypes(df)
    return df

