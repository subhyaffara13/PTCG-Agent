
def _get_buffer(
    buf: FilePath | WriteBuffer[str] | None, encoding: str | None = None
) -> Generator[WriteBuffer[str]] | Generator[StringIO]:
    """
    Context manager to open, yield and close buffer for filenames or Path-like
    objects, otherwise yield buf unchanged.
    """
    if buf is not None:
        buf = stringify_path(buf)
    else:
        buf = StringIO()

    if encoding is None:
        encoding = "utf-8"
    elif not isinstance(buf, str):
        raise ValueError("buf is not a file name and encoding is specified.")

    if hasattr(buf, "write"):
        # Incompatible types in "yield" (actual type "Union[str, WriteBuffer[str],
        # StringIO]", expected type "Union[WriteBuffer[str], StringIO]")
        yield buf  # type: ignore[misc]
    elif isinstance(buf, str):
        check_parent_directory(str(buf))
        with open(buf, "w", encoding=encoding, newline="") as f:
            # GH#30034 open instead of codecs.open prevents a file leak
            #  if we have an invalid encoding argument.
            # newline="" is needed to roundtrip correctly on
            #  windows test_to_latex_filename
            yield f
    else:
        raise TypeError("buf is not a file name and it has no write method")

