
def putchunk(fp: IO[bytes], cid: bytes, *data: bytes) -> None:
    """Write a PNG chunk (including CRC field)"""

    byte_data = b"".join(data)

    fp.write(o32(len(byte_data)) + cid)
    fp.write(byte_data)
    crc = _crc32(byte_data, _crc32(cid))
    fp.write(o32(crc))

