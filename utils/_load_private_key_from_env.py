
def _load_private_key_from_env(env_var: str) -> RSAPrivateKey:
    """Load an RSA private key from an env var (PEM string or file:// path)."""
    key_material = os.environ.get(env_var, "")
    if not key_material:
        raise ValueError(
            f"MCPJWTSigner: environment variable '{env_var}' is set but empty."
        )
    if key_material.startswith("file://"):
        path = key_material[len("file://") :]
        with open(path, "rb") as f:
            key_bytes = f.read()
    else:
        key_bytes = key_material.encode("utf-8")
    return serialization.load_pem_private_key(key_bytes, password=None)  # type: ignore[return-value]

