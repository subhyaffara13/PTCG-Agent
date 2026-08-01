
def _compute_kid(public_key: Any) -> str:
    """Derive a key ID from the public key's DER encoding (SHA-256, first 16 hex chars)."""
    der_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return hashlib.sha256(der_bytes).hexdigest()[:16]

