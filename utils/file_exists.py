
def file_exists(filepath_or_buffer: FilePath | BaseBuffer) -> bool:
    """Test whether file exists."""
    exists = False
    filepath_or_buffer = stringify_path(filepath_or_buffer)
    if not isinstance(filepath_or_buffer, str):
        return exists
    try:
        exists = os.path.exists(filepath_or_buffer)
        # gh-5874: if the filepath is too long will raise here
    except (TypeError, ValueError):
        pass
    return exists


def file_exists(path: Union[bytes, str, "os.PathLike[Text]"]) -> bool:
    """Validates file path as existing local file"""
    return os.path.isfile(path)

