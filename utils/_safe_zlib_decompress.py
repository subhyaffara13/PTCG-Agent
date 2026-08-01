
def _safe_zlib_decompress(s: bytes) -> bytes:
    dobj = zlib.decompressobj()
    plaintext = dobj.decompress(s, MAX_TEXT_CHUNK)
    if dobj.unconsumed_tail:
        msg = "Decompressed data too large for PngImagePlugin.MAX_TEXT_CHUNK"
        raise ValueError(msg)
    return plaintext

