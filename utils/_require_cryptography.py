
def _require_cryptography() -> None:
    if not _CRYPTOGRAPHY_AVAILABLE:
        raise ImportError(
            "cryptography package is required for OCI authentication. "
            "Please install it with: pip install cryptography"
        )

