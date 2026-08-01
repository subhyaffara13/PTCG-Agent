
def hash_digest(data: bytes) -> str:
    """Compute a hash digest of some data.

    We use a cryptographic hash because we want a low probability of
    accidental collision, but we don't really care about any of the
    cryptographic properties.
    """
    return hashlib.sha1(data).hexdigest()

