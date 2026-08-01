
def _safe_read(fp: IO[bytes], size: int) -> bytes:
    """
    Reads large blocks in a safe way.  Unlike fp.read(n), this function
    doesn't trust the user.  If the requested size is larger than
    SAFEBLOCK, the file is read block by block.

    :param fp: File handle.  Must implement a <b>read</b> method.
    :param size: Number of bytes to read.
    :returns: A string containing <i>size</i> bytes of data.

    Raises an OSError if the file is truncated and the read cannot be completed

    """
    if size <= 0:
        return b""
    if size <= SAFEBLOCK:
        data = fp.read(size)
        if len(data) < size:
            msg = "Truncated File Read"
            raise OSError(msg)
        return data
    blocks: list[bytes] = []
    remaining_size = size
    while remaining_size > 0:
        block = fp.read(min(remaining_size, SAFEBLOCK))
        if not block:
            break
        blocks.append(block)
        remaining_size -= len(block)
    if sum(len(block) for block in blocks) < size:
        msg = "Truncated File Read"
        raise OSError(msg)
    return b"".join(blocks)

