
def unpack_zipfile(filename, extract_dir, progress_filter=default_filter) -> None:
    """Unpack zip `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a zipfile (as determined
    by ``zipfile.is_zipfile()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """

    if not zipfile.is_zipfile(filename):
        raise UnrecognizedFormat(f"{filename} is not a zip file")

    with zipfile.ZipFile(filename) as z:
        _unpack_zipfile_obj(z, extract_dir, progress_filter)

