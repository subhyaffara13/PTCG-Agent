
def write_to_compressed(compression, path: str, data, dest: str = "test") -> None:
    """
    Write data to a compressed file.

    Parameters
    ----------
    compression : {'gzip', 'bz2', 'zip', 'xz', 'zstd'}
        The compression type to use.
    path : str
        The file path to write the data.
    data : str
        The data to write.
    dest : str, default "test"
        The destination file (for ZIP only)

    Raises
    ------
    ValueError : An invalid compression value was passed in.
    """
    args: tuple[Any, ...] = (data,)
    mode = "wb"
    method = "write"
    compress_method: Callable

    if compression == "zip":
        compress_method = zipfile.ZipFile
        mode = "w"
        args = (dest, data)
        method = "writestr"
    elif compression == "tar":
        compress_method = tarfile.TarFile
        mode = "w"
        file = tarfile.TarInfo(name=dest)
        bytes = io.BytesIO(data)
        file.size = len(data)
        args = (file, bytes)
        method = "addfile"
    elif compression == "gzip":
        compress_method = gzip.GzipFile
    elif compression == "bz2":
        import bz2

        compress_method = bz2.BZ2File
    elif compression == "zstd":
        compress_method = import_optional_dependency("zstandard").open
    elif compression == "xz":
        import lzma

        compress_method = lzma.LZMAFile
    else:
        raise ValueError(f"Unrecognized compression type: {compression}")

    # error: No overload variant of "ZipFile" matches argument types "str", "str"
    # error: No overload variant of "BZ2File" matches argument types "str", "str"
    # error: Argument "mode" to "TarFile" has incompatible type "str";
    #  expected "Literal['r', 'a', 'w', 'x']
    with compress_method(path, mode=mode) as f:  # type: ignore[call-overload, arg-type]
        getattr(f, method)(*args)

