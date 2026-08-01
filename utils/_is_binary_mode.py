
def _is_binary_mode(handle: FilePath | BaseBuffer, mode: str) -> bool:
    """Whether the handle is opened in binary mode"""
    # specified by user
    if "t" in mode or "b" in mode:
        return "b" in mode

    # exceptions
    text_classes = (
        # classes that expect string but have 'b' in mode
        codecs.StreamWriter,
        codecs.StreamReader,
        codecs.StreamReaderWriter,
    )
    if issubclass(type(handle), text_classes):
        return False

    return isinstance(handle, _get_binary_io_classes()) or "b" in getattr(
        handle, "mode", mode
    )

