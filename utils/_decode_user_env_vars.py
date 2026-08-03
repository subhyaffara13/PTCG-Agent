import json
from typing import Dict

def _decode_user_env_vars(stored: str) -> Dict[str, str]:
    """Decrypt a ``values_b64`` blob and parse it as a flat ``{name: value}`` dict."""
    decrypted = decrypt_value_helper(
        value=stored,
        key="mcp_user_env_vars",
        exception_type="debug",
        return_original_value=False,
    )
    if decrypted is None:
        if stored:
            verbose_proxy_logger.warning(
                "MCP per-user env vars failed to decrypt (LITELLM_SALT_KEY "
                "changed?); treating as unset so the user is prompted to "
                "re-enter them rather than silently forwarding ciphertext"
            )
        return {}
    try:
        parsed = json.loads(decrypted)
    except (ValueError, TypeError):
        return {}
    if not isinstance(parsed, dict):
        return {}
    return {str(k): str(v) for k, v in parsed.items()}

