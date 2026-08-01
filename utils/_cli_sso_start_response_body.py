
def _cli_sso_start_response_body(
    *,
    login_id: str,
    poll_secret: str,
    user_code: str,
    verification_uri_complete: str | None,
) -> dict[str, str | int]:
    if verification_uri_complete is None:
        return {
            "login_id": login_id,
            "poll_secret": poll_secret,
            "user_code": user_code,
            "expires_in": CLI_SSO_SESSION_TTL_SECONDS,
        }
    return {
        "login_id": login_id,
        "poll_secret": poll_secret,
        "user_code": user_code,
        "verification_uri_complete": verification_uri_complete,
        "expires_in": CLI_SSO_SESSION_TTL_SECONDS,
    }

