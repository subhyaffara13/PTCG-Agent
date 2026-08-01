
def _expiration_note(response: OAuthTokenResponse) -> str | None:
    """Human-readable note about the lifetime of a freshly obtained OAuth token, if known."""
    expires_in = response.get("expires_in")
    if not expires_in:
        return None
    if response.get("refresh_token"):
        return "This token will be refreshed automatically when it expires."
    days = max(1, int(expires_in) // 86400)
    return f"This token expires in {days} days. Log in again to renew it."

