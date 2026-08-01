
def _get_binary_io_classes() -> tuple[type, ...]:
    """IO classes that that expect bytes"""
    binary_classes: tuple[type, ...] = (BufferedIOBase, RawIOBase)

    # python-zstandard doesn't use any of the builtin base classes; instead we
    # have to use the `zstd.ZstdDecompressionReader` class for isinstance checks.
    # Unfortunately `zstd.ZstdDecompressionReader` isn't exposed by python-zstandard
    # so we have to get it from a `zstd.ZstdDecompressor` instance.
    # See also https://github.com/indygreg/python-zstandard/pull/165.
    zstd = import_optional_dependency("zstandard", errors="ignore")
    if zstd is not None:
        with zstd.ZstdDecompressor().stream_reader(b"") as reader:
            binary_classes += (type(reader),)

    return binary_classes

