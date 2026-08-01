
def get_handle(
    path_or_buf: FilePath | BaseBuffer,
    mode: str,
    *,
    encoding: str | None = ...,
    compression: CompressionOptions = ...,
    memory_map: bool = ...,
    is_text: Literal[False],
    errors: str | None = ...,
    storage_options: StorageOptions = ...,
) -> IOHandles[bytes]: ...


def get_handle(
    path_or_buf: FilePath | BaseBuffer,
    mode: str,
    *,
    encoding: str | None = ...,
    compression: CompressionOptions = ...,
    memory_map: bool = ...,
    is_text: Literal[True] = ...,
    errors: str | None = ...,
    storage_options: StorageOptions = ...,
) -> IOHandles[str]: ...


def get_handle(
    path_or_buf: FilePath | BaseBuffer,
    mode: str,
    *,
    encoding: str | None = ...,
    compression: CompressionOptions = ...,
    memory_map: bool = ...,
    is_text: bool = ...,
    errors: str | None = ...,
    storage_options: StorageOptions = ...,
) -> IOHandles[str] | IOHandles[bytes]: ...


def get_handle(
    path_or_buf: FilePath | BaseBuffer,
    mode: str,
    *,
    encoding: str | None = None,
    compression: CompressionOptions | None = None,
    memory_map: bool = False,
    is_text: bool = True,
    errors: str | None = None,
    storage_options: StorageOptions | None = None,
) -> IOHandles[str] | IOHandles[bytes]:
    """
    Get file handle for given path/buffer and mode.

    Parameters
    ----------
    path_or_buf : str or file handle
        File path or object.
    mode : str
        Mode to open path_or_buf with.
    encoding : str or None
        Encoding to use.
    compression : str or dict, default 'infer'
        For on-the-fly compression of the output data. If 'infer' and 'path_or_buf'
        is path-like, then detect compression from the following extensions: '.gz',
        '.bz2', '.zip', '.xz', '.zst', '.tar', '.tar.gz', '.tar.xz' or '.tar.bz2'
        (otherwise no compression).
        Set to ``None`` for no compression.
        Can also be a dict with key ``'method'`` set
        to one of {``'zip'``, ``'gzip'``, ``'bz2'``, ``'zstd'``, ``'xz'``, ``'tar'``}
        and other key-value pairs are forwarded to
        ``zipfile.ZipFile``, ``gzip.GzipFile``,
        ``bz2.BZ2File``, ``zstandard.ZstdCompressor``, ``lzma.LZMAFile`` or
        ``tarfile.TarFile``, respectively.
        As an example, the following could be passed for faster compression and to
        create a reproducible gzip archive:
        ``compression={'method': 'gzip', 'compresslevel': 1, 'mtime': 1}``.

           May be a dict with key 'method' as compression mode
           and other keys as compression options if compression
           mode is 'zip'.

           Passing compression options as keys in dict is
           supported for compression modes 'gzip', 'bz2', 'zstd' and 'zip'.

    memory_map : bool, default False
        See parsers._parser_params for more information. Only used by read_csv.
    is_text : bool, default True
        Whether the type of the content passed to the file/buffer is string or
        bytes. This is not the same as `"b" not in mode`. If a string content is
        passed to a binary file/buffer, a wrapper is inserted.
    errors : str, default 'strict'
        Specifies how encoding and decoding errors are to be handled.
        See the errors argument for :func:`open` for a full list
        of options.
    storage_options: StorageOptions = None
        Passed to _get_filepath_or_buffer

    Returns the dataclass IOHandles
    """
    # Windows does not default to utf-8. Set to utf-8 for a consistent behavior
    encoding = encoding or "utf-8"

    errors = errors or "strict"

    # read_csv does not know whether the buffer is opened in binary/text mode
    if _is_binary_mode(path_or_buf, mode) and "b" not in mode:
        mode += "b"

    # validate encoding and errors
    codecs.lookup(encoding)
    if isinstance(errors, str):
        codecs.lookup_error(errors)

    # open URLs
    ioargs = _get_filepath_or_buffer(
        path_or_buf,
        encoding=encoding,
        compression=compression,
        mode=mode,
        storage_options=storage_options,
    )

    handle = ioargs.filepath_or_buffer
    handles: list[BaseBuffer]

    # memory mapping needs to be the first step
    # only used for read_csv
    handle, memory_map, handles = _maybe_memory_map(handle, memory_map)

    is_path = isinstance(handle, str)
    compression_args = dict(ioargs.compression)
    compression = compression_args.pop("method")

    # Only for write methods
    if "r" not in mode and is_path:
        check_parent_directory(str(handle))

    if compression:
        if compression != "zstd":
            # compression libraries do not like an explicit text-mode
            ioargs.mode = ioargs.mode.replace("t", "")
        elif compression == "zstd" and "b" not in ioargs.mode:
            # python-zstandard defaults to text mode, but we always expect
            # compression libraries to use binary mode.
            ioargs.mode += "b"

        # GZ Compression
        if compression == "gzip":
            if isinstance(handle, str):
                # error: Incompatible types in assignment (expression has type
                # "GzipFile", variable has type "Union[str, BaseBuffer]")
                handle = gzip.GzipFile(  # type: ignore[assignment]
                    filename=handle,
                    mode=ioargs.mode,
                    **compression_args,
                )
            else:
                handle = gzip.GzipFile(
                    # No overload variant of "GzipFile" matches argument types
                    # "Union[str, BaseBuffer]", "str", "Dict[str, Any]"
                    fileobj=handle,  # type: ignore[call-overload]
                    mode=ioargs.mode,
                    **compression_args,
                )

        # BZ Compression
        elif compression == "bz2":
            import bz2

            # Overload of "BZ2File" to handle pickle protocol 5
            # "Union[str, BaseBuffer]", "str", "Dict[str, Any]"
            handle = bz2.BZ2File(  # type: ignore[call-overload]
                handle,
                mode=ioargs.mode,
                **compression_args,
            )

        # ZIP Compression
        elif compression == "zip":
            # error: Argument 1 to "_BytesZipFile" has incompatible type
            # "Union[str, BaseBuffer]"; expected "Union[Union[str, PathLike[str]],
            # ReadBuffer[bytes], WriteBuffer[bytes]]"
            handle = _BytesZipFile(
                handle,  # type: ignore[arg-type]
                ioargs.mode,
                **compression_args,
            )
            if handle.buffer.mode == "r":
                handles.append(handle)
                zip_names = handle.buffer.namelist()
                if len(zip_names) == 1:
                    handle = handle.buffer.open(zip_names.pop())
                elif not zip_names:
                    raise ValueError(f"Zero files found in ZIP file {path_or_buf}")
                else:
                    raise ValueError(
                        "Multiple files found in ZIP file. "
                        f"Only one file per ZIP: {zip_names}"
                    )

        # TAR Encoding
        elif compression == "tar":
            compression_args.setdefault("mode", ioargs.mode)
            if isinstance(handle, str):
                handle = _BytesTarFile(name=handle, **compression_args)
            else:
                # error: Argument "fileobj" to "_BytesTarFile" has incompatible
                # type "BaseBuffer"; expected "Union[ReadBuffer[bytes],
                # WriteBuffer[bytes], None]"
                handle = _BytesTarFile(
                    fileobj=handle,  # type: ignore[arg-type]
                    **compression_args,
                )
            assert isinstance(handle, _BytesTarFile)
            if "r" in handle.buffer.mode:
                handles.append(handle)
                files = handle.buffer.getnames()
                if len(files) == 1:
                    file = handle.buffer.extractfile(files[0])
                    assert file is not None
                    handle = file
                elif not files:
                    raise ValueError(f"Zero files found in TAR archive {path_or_buf}")
                else:
                    raise ValueError(
                        "Multiple files found in TAR archive. "
                        f"Only one file per TAR archive: {files}"
                    )

        # XZ Compression
        elif compression == "xz":
            # error: Argument 1 to "LZMAFile" has incompatible type "Union[str,
            # BaseBuffer]"; expected "Optional[Union[Union[str, bytes, PathLike[str],
            # PathLike[bytes]], IO[bytes]], None]"
            import lzma

            handle = lzma.LZMAFile(
                handle,  # type: ignore[arg-type]
                ioargs.mode,
                **compression_args,
            )

        # Zstd Compression
        elif compression == "zstd":
            zstd = import_optional_dependency("zstandard")
            if "r" in ioargs.mode:
                open_args = {"dctx": zstd.ZstdDecompressor(**compression_args)}
            else:
                open_args = {"cctx": zstd.ZstdCompressor(**compression_args)}
            handle = zstd.open(
                handle,
                mode=ioargs.mode,
                **open_args,
            )

        # Unrecognized Compression
        else:
            msg = f"Unrecognized compression type: {compression}"
            raise ValueError(msg)

        assert not isinstance(handle, str)
        handles.append(handle)

    elif isinstance(handle, str):
        # Check whether the filename is to be opened in binary mode.
        # Binary mode does not support 'encoding' and 'newline'.
        if ioargs.encoding and "b" not in ioargs.mode:
            # Encoding
            handle = open(
                handle,
                ioargs.mode,
                encoding=ioargs.encoding,
                errors=errors,
                newline="",
            )
        else:
            # Binary mode
            handle = open(handle, ioargs.mode)
        handles.append(handle)

    # Convert BytesIO or file objects passed with an encoding
    is_wrapped = False
    if not is_text and ioargs.mode == "rb" and isinstance(handle, TextIOBase):
        # not added to handles as it does not open/buffer resources
        handle = _BytesIOWrapper(
            handle,
            encoding=ioargs.encoding,
        )
    elif is_text and (
        compression or memory_map or _is_binary_mode(handle, ioargs.mode)
    ):
        if (
            not hasattr(handle, "readable")
            or not hasattr(handle, "writable")
            or not hasattr(handle, "seekable")
        ):
            handle = _IOWrapper(handle)
        # error: Value of type variable "_BufferT_co" of "TextIOWrapper" cannot
        # be "_IOWrapper | BaseBuffer" [type-var]
        handle = TextIOWrapper(
            handle,  # type: ignore[type-var]
            encoding=ioargs.encoding,
            errors=errors,
            newline="",
        )
        handles.append(handle)
        # only marked as wrapped when the caller provided a handle
        is_wrapped = not (
            isinstance(ioargs.filepath_or_buffer, str) or ioargs.should_close
        )

    if "r" in ioargs.mode and not hasattr(handle, "read"):
        raise TypeError(
            "Expected file path name or file-like object, "
            f"got {type(ioargs.filepath_or_buffer)} type"
        )

    handles.reverse()  # close the most recently added buffer first
    if ioargs.should_close:
        assert not isinstance(ioargs.filepath_or_buffer, str)
        handles.append(ioargs.filepath_or_buffer)
        handles.extend(ioargs.close_handles)

    return IOHandles(
        # error: Argument "handle" to "IOHandles" has incompatible type
        # "Union[TextIOWrapper, GzipFile, BaseBuffer, typing.IO[bytes],
        # typing.IO[Any]]"; expected "pandas._typing.IO[Any]"
        handle=handle,  # type: ignore[arg-type]
        # error: Argument "created_handles" to "IOHandles" has incompatible type
        # "List[BaseBuffer]"; expected "List[Union[IO[bytes], IO[str]]]"
        created_handles=handles,  # type: ignore[arg-type]
        is_wrapped=is_wrapped,
        compression=ioargs.compression,
    )

