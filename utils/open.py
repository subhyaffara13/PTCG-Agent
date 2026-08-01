
def open(
    urlpath,
    mode="rb",
    compression=None,
    encoding="utf8",
    errors=None,
    protocol=None,
    newline=None,
    expand=None,
    **kwargs,
):
    """Given a path or paths, return one ``OpenFile`` object.

    Parameters
    ----------
    urlpath: string or list
        Absolute or relative filepath. Prefix with a protocol like ``s3://``
        to read from alternative filesystems. Should not include glob
        character(s).
    mode: 'rb', 'wt', etc.
    compression: string or None
        If given, open file using compression codec. Can either be a compression
        name (a key in ``fsspec.compression.compr``) or "infer" to guess the
        compression from the filename suffix.
    encoding: str
        For text mode only
    errors: None or str
        Passed to TextIOWrapper in text mode
    protocol: str or None
        If given, overrides the protocol found in the URL.
    newline: bytes or None
        Used for line terminator in text mode. If None, uses system default;
        if blank, uses no translation.
    expand: bool or None
        Whether to regard file paths containing special glob characters as needing
        expansion (finding the first match) or absolute. Setting False allows using
        paths which do embed such characters. If None (default), this argument
        takes its value from the DEFAULT_EXPAND module variable, which takes
        its initial value from the "open_expand" config value at startup, which will
        be False if not set.
    **kwargs: dict
        Extra options that make sense to a particular storage connection, e.g.
        host, port, username, password, etc.

    Examples
    --------
    >>> openfile = open('2015-01-01.csv')  # doctest: +SKIP
    >>> openfile = open(
    ...     's3://bucket/2015-01-01.csv.gz', compression='gzip'
    ... )  # doctest: +SKIP
    >>> with openfile as f:
    ...     df = pd.read_csv(f)  # doctest: +SKIP
    ...

    Returns
    -------
    ``OpenFile`` object.

    Notes
    -----
    For a full list of the available protocols and the implementations that
    they map across to see the latest online documentation:

    - For implementations built into ``fsspec`` see
      https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations
    - For implementations in separate packages see
      https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations
    """
    expand = DEFAULT_EXPAND if expand is None else expand
    out = open_files(
        urlpath=[urlpath],
        mode=mode,
        compression=compression,
        encoding=encoding,
        errors=errors,
        protocol=protocol,
        newline=newline,
        expand=expand,
        **kwargs,
    )
    if not out:
        raise FileNotFoundError(urlpath)
    return out[0]


def open(fp: StrOrBytesPath | IO[bytes], mode: str = "r") -> GdImageFile:
    """
    Load texture from a GD image file.

    :param fp: GD file name, or an opened file handle.
    :param mode: Optional mode.  In this version, if the mode argument
        is given, it must be "r".
    :returns: An image instance.
    :raises OSError: If the image could not be read.
    """
    if mode != "r":
        msg = "bad mode"
        raise ValueError(msg)

    try:
        return GdImageFile(fp)
    except SyntaxError as e:
        msg = "cannot identify this image file"
        raise UnidentifiedImageError(msg) from e


def open(
    fp: StrOrBytesPath | IO[bytes],
    mode: Literal["r"] = "r",
    formats: list[str] | tuple[str, ...] | None = None,
) -> ImageFile.ImageFile:
    """
    Opens and identifies the given image file.

    This is a lazy operation; this function identifies the file, but
    the file remains open and the actual image data is not read from
    the file until you try to process the data (or call the
    :py:meth:`~PIL.Image.Image.load` method).  See
    :py:func:`~PIL.Image.new`. See :ref:`file-handling`.

    :param fp: A filename (string), os.PathLike object or a file object.
       The file object must implement ``file.read``,
       ``file.seek``, and ``file.tell`` methods,
       and be opened in binary mode. The file object will also seek to zero
       before reading.
    :param mode: The mode.  If given, this argument must be "r".
    :param formats: A list or tuple of formats to attempt to load the file in.
       This can be used to restrict the set of formats checked.
       Pass ``None`` to try all supported formats. You can print the set of
       available formats by running ``python3 -m PIL`` or using
       the :py:func:`PIL.features.pilinfo` function.
    :returns: An :py:class:`~PIL.Image.Image` object.
    :exception FileNotFoundError: If the file cannot be found.
    :exception PIL.UnidentifiedImageError: If the image cannot be opened and
       identified.
    :exception ValueError: If the ``mode`` is not "r", or if a ``StringIO``
       instance is used for ``fp``.
    :exception TypeError: If ``formats`` is not ``None``, a list or a tuple.
    """

    if mode != "r":
        msg = f"bad mode {repr(mode)}"  # type: ignore[unreachable]
        raise ValueError(msg)
    elif isinstance(fp, io.StringIO):
        msg = (  # type: ignore[unreachable]
            "StringIO cannot be used to open an image. "
            "Binary data must be used instead."
        )
        raise ValueError(msg)

    if formats is None:
        formats = ID
    elif not isinstance(formats, (list, tuple)):
        msg = "formats must be a list or tuple"  # type: ignore[unreachable]
        raise TypeError(msg)

    exclusive_fp = False
    filename: str | bytes = ""
    if is_path(fp):
        filename = os.fspath(fp)
        fp = builtins.open(filename, "rb")
        exclusive_fp = True
    else:
        fp = cast(IO[bytes], fp)

    try:
        fp.seek(0)
    except (AttributeError, io.UnsupportedOperation):
        fp = io.BytesIO(fp.read())
        exclusive_fp = True

    prefix = fp.read(16)

    # Try to import just the plugin needed for this file extension
    # before falling back to preinit() which imports common plugins
    ext = os.path.splitext(filename)[1] if filename else ""
    if not _import_plugin_for_extension(ext):
        preinit()

    warning_messages: list[str] = []

    def _open_core(
        fp: IO[bytes],
        filename: str | bytes,
        prefix: bytes,
        formats: list[str] | tuple[str, ...],
    ) -> ImageFile.ImageFile | None:
        for i in formats:
            i = i.upper()
            if i not in OPEN:
                init()
            try:
                factory, accept = OPEN[i]
                result = not accept or accept(prefix)
                if isinstance(result, str):
                    warning_messages.append(result)
                elif result:
                    fp.seek(0)
                    im = factory(fp, filename)
                    _decompression_bomb_check(im.size)
                    return im
            except (SyntaxError, IndexError, TypeError, struct.error) as e:
                if WARN_POSSIBLE_FORMATS:
                    warning_messages.append(i + " opening failed. " + str(e))
            except BaseException:
                if exclusive_fp:
                    fp.close()
                raise
        return None

    im = _open_core(fp, filename, prefix, formats)

    if im is None and formats is ID:
        # Try preinit (few common plugins) then init (all plugins)
        for loader in (preinit, init):
            checked_formats = ID.copy()
            loader()
            if formats != checked_formats:
                im = _open_core(
                    fp,
                    filename,
                    prefix,
                    tuple(f for f in formats if f not in checked_formats),
                )
                if im is not None:
                    break

    if im:
        im._exclusive_fp = exclusive_fp
        return im

    if exclusive_fp:
        fp.close()
    for message in warning_messages:
        warnings.warn(message)
    msg = "cannot identify image file %r" % (filename if filename else fp)
    raise UnidentifiedImageError(msg)


def open(filename: StrOrBytesPath | IO[bytes]) -> WalImageFile:
    """
    Load texture from a Quake2 WAL texture file.

    By default, a Quake2 standard palette is attached to the texture.
    To override the palette, use the :py:func:`PIL.Image.Image.putpalette()` method.

    :param filename: WAL file name, or an opened file handle.
    :returns: An image instance.
    """
    return WalImageFile(filename)


def open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Union[Literal["rt"], Literal["r"]],
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
) -> ContextManager[TextIO]:
    pass


def open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Literal["rb"],
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
) -> ContextManager[BinaryIO]:
    pass


def open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Union[Literal["rb"], Literal["rt"], Literal["r"]] = "r",
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
) -> Union[ContextManager[BinaryIO], ContextManager[TextIO]]:
    """Read bytes from a file while tracking progress.

    Args:
        path (Union[str, PathLike[str], BinaryIO]): The path to the file to read, or a file-like object in binary mode.
        mode (str): The mode to use to open the file. Only supports "r", "rb" or "rt".
        buffering (int): The buffering strategy to use, see :func:`io.open`.
        encoding (str, optional): The encoding to use when reading in text mode, see :func:`io.open`.
        errors (str, optional): The error handling strategy for decoding errors, see :func:`io.open`.
        newline (str, optional): The strategy for handling newlines in text mode, see :func:`io.open`
        total: (int, optional): Total number of bytes to read. Must be provided if reading from a file handle. Default for a path is os.stat(file).st_size.
        description (str, optional): Description of task show next to progress bar. Defaults to "Reading".
        auto_refresh (bool, optional): Automatic refresh, disable to force a refresh after each iteration. Default is True.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        console (Console, optional): Console to write to. Default creates internal Console instance.
        refresh_per_second (float): Number of times per second to refresh the progress information. Defaults to 10.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.finished".
        pulse_style (StyleType, optional): Style for pulsing bars. Defaults to "bar.pulse".
        disable (bool, optional): Disable display of progress.
        encoding (str, optional): The encoding to use when reading in text mode.

    Returns:
        ContextManager[BinaryIO]: A context manager yielding a progress reader.

    """

    columns: List["ProgressColumn"] = (
        [TextColumn("[progress.description]{task.description}")] if description else []
    )
    columns.extend(
        (
            BarColumn(
                style=style,
                complete_style=complete_style,
                finished_style=finished_style,
                pulse_style=pulse_style,
            ),
            DownloadColumn(),
            TimeRemainingColumn(),
        )
    )
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        get_time=get_time,
        refresh_per_second=refresh_per_second or 10,
        disable=disable,
    )

    reader = progress.open(
        file,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        total=total,
        description=description,
    )
    return _ReadContext(progress, reader)  # type: ignore[return-value, type-var]


def open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Union[Literal["rt"], Literal["r"]],
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
) -> ContextManager[TextIO]:
    pass


def open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Literal["rb"],
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
) -> ContextManager[BinaryIO]:
    pass


def open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Union[Literal["rb"], Literal["rt"], Literal["r"]] = "r",
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
) -> Union[ContextManager[BinaryIO], ContextManager[TextIO]]:
    """Read bytes from a file while tracking progress.

    Args:
        path (Union[str, PathLike[str], BinaryIO]): The path to the file to read, or a file-like object in binary mode.
        mode (str): The mode to use to open the file. Only supports "r", "rb" or "rt".
        buffering (int): The buffering strategy to use, see :func:`io.open`.
        encoding (str, optional): The encoding to use when reading in text mode, see :func:`io.open`.
        errors (str, optional): The error handling strategy for decoding errors, see :func:`io.open`.
        newline (str, optional): The strategy for handling newlines in text mode, see :func:`io.open`
        total: (int, optional): Total number of bytes to read. Must be provided if reading from a file handle. Default for a path is os.stat(file).st_size.
        description (str, optional): Description of task show next to progress bar. Defaults to "Reading".
        auto_refresh (bool, optional): Automatic refresh, disable to force a refresh after each iteration. Default is True.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        console (Console, optional): Console to write to. Default creates internal Console instance.
        refresh_per_second (float): Number of times per second to refresh the progress information. Defaults to 10.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.finished".
        pulse_style (StyleType, optional): Style for pulsing bars. Defaults to "bar.pulse".
        disable (bool, optional): Disable display of progress.
        encoding (str, optional): The encoding to use when reading in text mode.

    Returns:
        ContextManager[BinaryIO]: A context manager yielding a progress reader.

    """

    columns: List["ProgressColumn"] = (
        [TextColumn("[progress.description]{task.description}")] if description else []
    )
    columns.extend(
        (
            BarColumn(
                style=style,
                complete_style=complete_style,
                finished_style=finished_style,
                pulse_style=pulse_style,
            ),
            DownloadColumn(),
            TimeRemainingColumn(),
        )
    )
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        get_time=get_time,
        refresh_per_second=refresh_per_second or 10,
        disable=disable,
    )

    reader = progress.open(
        file,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        total=total,
        description=description,
    )
    return _ReadContext(progress, reader)  # type: ignore[return-value, type-var]


def open(path, mode='r', destpath=os.curdir, encoding=None, newline=None):
    """
    Open `path` with `mode` and return the file object.

    If ``path`` is a URL, it will be downloaded, stored in the
    `DataSource` `destpath` directory and opened from there.

    Parameters
    ----------
    path : str or pathlib.Path
        Local file path or URL to open.
    mode : str, optional
        Mode to open `path`. Mode 'r' for reading, 'w' for writing, 'a' to
        append. Available modes depend on the type of object specified by
        path.  Default is 'r'.
    destpath : str, optional
        Path to the directory where the source file gets downloaded to for
        use.  If `destpath` is None, a temporary directory will be created.
        The default path is the current directory.
    encoding : {None, str}, optional
        Open text file with given encoding. The default encoding will be
        what `open` uses.
    newline : {None, str}, optional
        Newline to use when reading text file.

    Returns
    -------
    out : file object
        The opened file.

    Notes
    -----
    This is a convenience function that instantiates a `DataSource` and
    returns the file object from ``DataSource.open(path)``.

    """

    ds = DataSource(destpath)
    return ds.open(path, mode, encoding=encoding, newline=newline)


def open(
    file,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
    *,
    loop=None,
    executor=None,
):
    return AiofilesContextManager(
        _open(
            file,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
            loop=loop,
            executor=executor,
        )
    )

