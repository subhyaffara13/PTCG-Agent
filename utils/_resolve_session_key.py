import json
from typing import Any, Dict, Optional

def _resolve_session_key(kwargs: Dict[str, Any]) -> Optional[str]:
    """Pick a stable per-conversation key for owner-cache attribution.

    Order:
      1. Honor a client-supplied session id (`litellm_session_id` on either
         `litellm_params` or `litellm_params.metadata`, or `session_id` on
         metadata) — backward compat for callers already wired up.
      2. Otherwise derive a sha256 over (identity fields, first
         SIGNAL_GATE_MIN_MESSAGES messages) so the key is stable across turns
         and only materialises once there is enough context for the bandit to
         act on (matching the gate in the signal-processing path).

    Returns None if the conversation is shorter than SIGNAL_GATE_MIN_MESSAGES.
    """
    litellm_params = kwargs.get("litellm_params") or {}
    sid = litellm_params.get("litellm_session_id")
    if sid:
        return str(sid)
    metadata = litellm_params.get("metadata") or {}
    if isinstance(metadata, dict):
        sid = metadata.get("session_id") or metadata.get("litellm_session_id")
        if sid:
            return str(sid)

    messages = kwargs.get("messages") or []
    if len(messages) < SIGNAL_GATE_MIN_MESSAGES:
        # Don't attribute until we have enough turns to match the signal gate —
        # ensures the hash is stable (same N messages every time) and avoids
        # crediting the bandit for conversations that are too short to signal.
        return None

    identity = ":".join(
        str(metadata.get(f) or "") if isinstance(metadata, dict) else ""
        for f in _IDENTITY_FIELDS
    )
    anchor = messages[:SIGNAL_GATE_MIN_MESSAGES]
    payload = (
        identity
        + "|"
        + json.dumps(
            [{"role": m.get("role"), "content": m.get("content")} for m in anchor],
            sort_keys=True,
            default=str,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

