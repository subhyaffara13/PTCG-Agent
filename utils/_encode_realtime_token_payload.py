
def _encode_realtime_token_payload(
    ephemeral_key: str,
    model_id: str,
    user_id: Optional[str],
    team_id: Optional[str],
    expires_at: Optional[int],
    session_type: str = "realtime",
) -> str:
    """
    Encode metadata with the upstream ephemeral key so /realtime/calls can
    route without requiring model as a query param.
    """
    payload: Dict[str, Any] = {
        "v": _REALTIME_TOKEN_VERSION,
        "ephemeral_key": ephemeral_key,
        "model_id": model_id,
        "user_id": user_id or "",
        "team_id": team_id or "",
        "expires_at": expires_at,
        "session_type": session_type,
    }
    return json.dumps(payload, separators=(",", ":"))

