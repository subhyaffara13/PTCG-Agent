
def extract_files(
    # TODO: this needs to take Dict but variance issues.....
    # create protocol type ?
    query: Mapping[str, object],
    *,
    paths: Sequence[Sequence[str]],
    array_format: ArrayFormat = "brackets",
) -> list[tuple[str, FileTypes]]:
    """Recursively extract files from the given dictionary based on specified paths.

    A path may look like this ['foo', 'files', '<array>', 'data'].

    ``array_format`` controls how ``<array>`` segments contribute to the emitted
    field name. Supported values: ``"brackets"`` (``foo[]``), ``"repeat"`` and
    ``"comma"`` (``foo``), ``"indices"`` (``foo[0]``, ``foo[1]``).

    Note: this mutates the given dictionary.
    """
    files: list[tuple[str, FileTypes]] = []
    for path in paths:
        files.extend(_extract_items(query, path, index=0, flattened_key=None, array_format=array_format))
    return files

