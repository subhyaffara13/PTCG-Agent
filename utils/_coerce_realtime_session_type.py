
def _coerce_realtime_session_type(session_type: Optional[str]) -> str:
    if session_type in _ALLOWED_SESSION_TYPES:
        return session_type
    return "realtime"

