import json
from typing import Any, Dict, Optional

def _decode_realtime_token_payload(
    decrypted_value: str,
) -> Optional[Dict[str, Any]]:
    """
    Decode realtime token payload; returns None for legacy/raw ephemeral tokens.
    """
    try:
        decoded = json.loads(decrypted_value)
    except Exception:
        return None

    if not isinstance(decoded, dict):
        return None
    if decoded.get("v") != _REALTIME_TOKEN_VERSION:
        return None
    if not isinstance(decoded.get("ephemeral_key"), str):
        return None
    if not isinstance(decoded.get("model_id"), str):
        return None
    return decoded

