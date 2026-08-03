from typing import Any, Dict

def is_oauth_credential_expired(cred: Dict[str, Any], buffer_seconds: int = 0) -> bool:
    """Return True if the OAuth2 credential's access_token has expired.

    Checks the ``expires_at`` ISO-format string stored in the credential payload.
    Returns False when ``expires_at`` is absent or unparseable (treat as non-expired).
    With ``buffer_seconds`` > 0, a token that is still valid but expires within the
    buffer is also treated as expired, so callers can refresh proactively instead of
    handing back a token that may lapse mid-request.
    """
    expires_at = cred.get("expires_at")
    if not expires_at:
        return False
    try:
        exp_dt = datetime.fromisoformat(expires_at)
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) + timedelta(seconds=buffer_seconds) > exp_dt
    except (ValueError, TypeError):
        return False

