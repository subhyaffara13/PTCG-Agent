
def _open_zipfile_writer(name_or_buffer: str | IO[bytes]) -> _opener:
    container: type[_opener]
    if _is_path(name_or_buffer):
        container = _open_zipfile_writer_file
    else:
        container = _open_zipfile_writer_buffer
    return container(name_or_buffer)  # type: ignore[arg-type]

