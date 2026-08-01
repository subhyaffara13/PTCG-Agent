
def _open_file_like(name_or_buffer: FileLike, mode: str) -> _opener[IO[bytes]]:
    if _is_path(name_or_buffer):
        return _open_file(name_or_buffer, mode)
    else:
        if "w" in mode:
            return _open_buffer_writer(name_or_buffer)
        elif "r" in mode:
            return _open_buffer_reader(name_or_buffer)
        else:
            raise RuntimeError(f"Expected 'r' or 'w' in mode but got {mode}")

