
def _compute_sha256_digest(to_be_signed, to_be_signed_len):
    from cryptography.hazmat.primitives import hashes

    data = ctypes.string_at(to_be_signed, to_be_signed_len)
    hash = hashes.Hash(hashes.SHA256())
    hash.update(data)
    return hash.finalize()

