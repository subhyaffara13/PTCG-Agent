
def load_private_key_from_str(key_str: str) -> Any:
    _require_cryptography()
    key = serialization.load_pem_private_key(  # type: ignore[union-attr]
        key_str.encode("utf-8"),
        password=None,
    )
    if not isinstance(key, rsa.RSAPrivateKey):  # type: ignore[union-attr]
        raise TypeError(
            "The provided private key is not an RSA key, which is required for OCI signing."
        )
    return key

