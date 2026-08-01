
def hash_digest_bytes(data: bytes) -> bytes:
    """Compute a hash digest of some data.

    Similar to above but returns a bytes object.
    """
    return hashlib.sha1(data).digest()

