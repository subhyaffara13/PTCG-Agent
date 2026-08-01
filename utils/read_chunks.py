
def read_chunks(file: BinaryIO, size: int = io.DEFAULT_BUFFER_SIZE) -> Iterator[bytes]:
    """Yield pieces of data from a file-like object until EOF."""
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk


def read_chunks(
    file: BinaryIO, size: int = FILE_CHUNK_SIZE
) -> Generator[bytes, None, None]:
    """Yield pieces of data from a file-like object until EOF."""
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk

