
def copy_file_data(src_file: IO, dst_file: IO, chunk_size: int | None = None):
    """Copy data from one file object to another."""
    _chunk_size = 1024 * 1024 if chunk_size is None else chunk_size
    read = src_file.read
    write = dst_file.write
    # in iter(callable, sentilel), callable is called until it returns the sentinel;
    # this allows to copy `chunk_size` bytes at a time.
    for chunk in iter(lambda: read(_chunk_size) or None, None):
        write(chunk)

