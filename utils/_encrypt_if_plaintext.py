from typing import Any

def _encrypt_if_plaintext(key: str, value: Any) -> Any:
    if not isinstance(value, str) or not value:
        return value
    if not _is_sensitive_callback_var(key):
        return value
    if value.startswith(_CALLBACK_VAR_ENCRYPTED_PREFIX):
        # Already encrypted — round-tripping ciphertext (e.g. UI Edit Settings
        # save without changing the field) must not double-encrypt. Cheap
        # prefix check is robust under salt-key rotation; a decrypt-based
        # idempotency check would mis-classify K1-encrypted blobs as
        # plaintext under K2 and wrap them a second time.
        return value
    try:
        return _CALLBACK_VAR_ENCRYPTED_PREFIX + encrypt_value_helper(value)
    except Exception:
        # No salt key / master key configured — leave the value as-is rather
        # than crash the write. Dev environments without LITELLM_SALT_KEY hit
        # this path; production always has a master key so encryption proceeds.
        return value

