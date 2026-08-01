
def encrypt_callback_vars(metadata: Any) -> Any:
    """Return a deep copy of metadata with callback_vars values encrypted at rest.

    Idempotent: a value that already decrypts cleanly is left unchanged so
    round-trips through edit forms don't double-encrypt.
    """
    return _transform_callback_vars(metadata, _encrypt_if_plaintext)

