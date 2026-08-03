from typing import Any

def decrypt_callback_vars(metadata: Any) -> Any:
    """Return a deep copy of metadata with callback_vars values decrypted.

    Legacy plaintext rows pass through unchanged (decrypt failure → original).
    """
    return _transform_callback_vars(metadata, _decrypt_or_passthrough)

