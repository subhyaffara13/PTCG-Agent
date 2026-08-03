from typing import Any

def _payload_to_action_string(payload: Mapping[str, Any]) -> str | None:
    """Convert a parsed JSON dict into a canonical legal-action string.

    Returns ``None`` if the dict doesn't look like a valid bargaining
    action (missing keys, non-integer counts, etc.). Returns a string
    even if the action would be illegal in the current state -- the
    caller verifies legality against ``legal_action_strings``.
    """
    action = str(payload.get("action", "")).strip().lower() if payload.get("action") is not None else ""

    if action == "agree" or action == "accept" or payload.get("agree") is True:
        return _AGREE_ACTION_STRING

    keep_obj = payload.get("keep") or payload.get("items") or payload.get("offer")
    if not isinstance(keep_obj, Mapping):
        return None
    normalized = _normalize_keep(keep_obj)
    try:
        counts = {k: int(normalized.get(k, 0)) for k in _ITEM_KEYS}
    except (TypeError, ValueError):
        return None
    if any(v < 0 for v in counts.values()):
        return None
    return f"Offer: Book: {counts['book']}, Hat: {counts['hat']}, Basketball: {counts['basketball']}"

