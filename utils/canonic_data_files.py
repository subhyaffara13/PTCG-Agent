
def canonic_data_files(
    data_files: list | dict, root_dir: StrPath | None = None
) -> list[tuple[str, list[str]]]:
    """For compatibility with ``setup.py``, ``data_files`` should be a list
    of pairs instead of a dict.

    This function also expands glob patterns.
    """
    if isinstance(data_files, list):
        return data_files

    return [
        (dest, glob_relative(patterns, root_dir))
        for dest, patterns in data_files.items()
    ]

