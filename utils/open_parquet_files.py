
def open_parquet_files(
    path: list[str],
    fs: None | fsspec.AbstractFileSystem = None,
    metadata=None,
    columns: None | list[str] = None,
    row_groups: None | list[int] = None,
    storage_options: None | dict = None,
    engine: str = "auto",
    max_gap: int = 64_000,
    max_block: int = 256_000_000,
    footer_sample_size: int = 1_000_000,
    filters: None | list[list[list[str]]] = None,
    **kwargs,
):
    """
    Return a file-like object for a single Parquet file.

    The specified parquet `engine` will be used to parse the
    footer metadata, and determine the required byte ranges
    from the file. The target path will then be opened with
    the "parts" (`KnownPartsOfAFile`) caching strategy.

    Note that this method is intended for usage with remote
    file systems, and is unlikely to improve parquet-read
    performance on local file systems.

    Parameters
    ----------
    path: str
        Target file path.
    metadata: Any, optional
        Parquet metadata object. Object type must be supported
        by the backend parquet engine. For now, only the "fastparquet"
        engine supports an explicit `ParquetFile` metadata object.
        If a metadata object is supplied, the remote footer metadata
        will not need to be transferred into local memory.
    fs: AbstractFileSystem, optional
        Filesystem object to use for opening the file. If nothing is
        specified, an `AbstractFileSystem` object will be inferred.
    engine : str, default "auto"
        Parquet engine to use for metadata parsing. Allowed options
        include "fastparquet", "pyarrow", and "auto". The specified
        engine must be installed in the current environment. If
        "auto" is specified, and both engines are installed,
        "fastparquet" will take precedence over "pyarrow".
    columns: list, optional
        List of all column names that may be read from the file.
    row_groups : list, optional
        List of all row-groups that may be read from the file. This
        may be a list of row-group indices (integers), or it may be
        a list of `RowGroup` metadata objects (if the "fastparquet"
        engine is used).
    storage_options : dict, optional
        Used to generate an `AbstractFileSystem` object if `fs` was
        not specified.
    max_gap : int, optional
        Neighboring byte ranges will only be merged when their
        inter-range gap is <= `max_gap`. Default is 64KB.
    max_block : int, optional
        Neighboring byte ranges will only be merged when the size of
        the aggregated range is <= `max_block`. Default is 256MB.
    footer_sample_size : int, optional
        Number of bytes to read from the end of the path to look
        for the footer metadata. If the sampled bytes do not contain
        the footer, a second read request will be required, and
        performance will suffer. Default is 1MB.
    filters : list[list], optional
        List of filters to apply to prevent reading row groups, of the
        same format as accepted by the loading engines. Ignored if
        ``row_groups`` is specified.
    **kwargs :
        Optional key-word arguments to pass to `fs.open`
    """

    # Make sure we have an `AbstractFileSystem` object
    # to work with
    if fs is None:
        path0 = path
        if isinstance(path, (list, tuple)):
            path = path[0]
        fs, path = url_to_fs(path, **(storage_options or {}))
    else:
        path0 = path

    # For now, `columns == []` not supported, is the same
    # as all columns
    if columns is not None and len(columns) == 0:
        columns = None

    # Set the engine
    engine = _set_engine(engine)

    if isinstance(path0, (list, tuple)):
        paths = path0
    elif "*" in path:
        paths = fs.glob(path)
    elif path0.endswith("/"):  # or fs.isdir(path):
        paths = [
            _
            for _ in fs.find(path, withdirs=False, detail=False)
            if _.endswith((".parquet", ".parq"))
        ]
    else:
        paths = [path]

    data = _get_parquet_byte_ranges(
        paths,
        fs,
        metadata=metadata,
        columns=columns,
        row_groups=row_groups,
        engine=engine,
        max_gap=max_gap,
        max_block=max_block,
        footer_sample_size=footer_sample_size,
        filters=filters,
    )

    # Call self.open with "parts" caching
    options = kwargs.pop("cache_options", {}).copy()
    return [
        AlreadyBufferedFile(
            fs=None,
            path=fn,
            mode="rb",
            cache_type="parts",
            cache_options={
                **options,
                "data": ranges,
            },
            size=max(_[1] for _ in ranges),
            **kwargs,
        )
        for fn, ranges in data.items()
    ]

