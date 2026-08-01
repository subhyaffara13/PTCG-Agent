
def getchunks(im: Image.Image, **params: Any) -> list[tuple[bytes, bytes, bytes]]:
    """Return a list of PNG chunks representing this image."""
    from io import BytesIO

    chunks = []

    def append(fp: IO[bytes], cid: bytes, *data: bytes) -> None:
        byte_data = b"".join(data)
        crc = o32(_crc32(byte_data, _crc32(cid)))
        chunks.append((cid, byte_data, crc))

    fp = BytesIO()

    try:
        im.encoderinfo = params
        _save(im, fp, "", append)
    finally:
        del im.encoderinfo

    return chunks

