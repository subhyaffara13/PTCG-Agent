from typing import Any

def _decrypt_or_passthrough(key: str, value: Any) -> Any:
    if not isinstance(value, str) or not value:
        return value
    if not value.startswith(_CALLBACK_VAR_ENCRYPTED_PREFIX):
        # Legacy plaintext rows or non-credential fields — return as-is.
        return value
    inner = value[len(_CALLBACK_VAR_ENCRYPTED_PREFIX) :]
    decrypted = decrypt_value_helper(
        value=inner, key=key, exception_type="debug", return_original_value=False
    )
    return decrypted if decrypted is not None else value

