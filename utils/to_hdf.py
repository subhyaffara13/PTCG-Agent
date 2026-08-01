
def to_hdf(
    path_or_buf: FilePath | HDFStore,
    key: str,
    value: DataFrame | Series,
    mode: str = "a",
    complevel: int | None = None,
    complib: str | None = None,
    append: bool = False,
    format: str | None = None,
    index: bool = True,
    min_itemsize: int | dict[str, int] | None = None,
    nan_rep=None,
    dropna: bool | None = None,
    data_columns: Literal[True] | list[str] | None = None,
    errors: str = "strict",
    encoding: str = "UTF-8",
) -> None:
    """store this object, close it if we opened it"""
    if append:
        f = lambda store: store.append(
            key,
            value,
            format=format,
            index=index,
            min_itemsize=min_itemsize,
            nan_rep=nan_rep,
            dropna=dropna,
            data_columns=data_columns,
            errors=errors,
            encoding=encoding,
        )
    else:
        # NB: dropna is not passed to `put`
        f = lambda store: store.put(
            key,
            value,
            format=format,
            index=index,
            min_itemsize=min_itemsize,
            nan_rep=nan_rep,
            data_columns=data_columns,
            errors=errors,
            encoding=encoding,
            dropna=dropna,
        )

    if isinstance(path_or_buf, HDFStore):
        f(path_or_buf)
    else:
        path_or_buf = stringify_path(path_or_buf)
        with HDFStore(
            path_or_buf, mode=mode, complevel=complevel, complib=complib
        ) as store:
            f(store)

