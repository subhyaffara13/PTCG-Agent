from typing import Optional

def _user_id_from_session_cookie(request: Request) -> Optional[str]:
    """Return user_id from the UI ``token`` cookie (HS256-signed with
    ``master_key``), or None if missing/invalid.

    The /token endpoint in this file ALSO issues master-key-signed JWTs
    (type="byok_session") for MCP-client-side use. They must not be
    accepted here as UI sessions — otherwise a leaked byok_session token
    could be replayed as a cookie to re-authorize BYOK writes. Distinguish
    by requiring a ``login_method`` claim (UI tokens set ``"sso"`` or
    ``"username_password"``; byok_session tokens never set it) and
    rejecting any token whose ``type`` identifies it as non-UI.
    """
    # Inline import avoids a circular dep (proxy_server -> mcp_server router).
    from litellm.proxy.proxy_server import master_key

    if not master_key:
        return None
    token = request.cookies.get("token")
    if not token:
        return None
    try:
        payload = jwt.decode(
            token,
            master_key,
            algorithms=["HS256"],
            # Require an expiry claim so a leaked UI session cookie has a
            # bounded lifetime. PyJWT verifies exp by default when present;
            # require=["exp"] additionally rejects tokens that omit it.
            options={"require": ["exp"]},
        )
    except jwt.InvalidTokenError:
        return None
    if payload.get("type") == "byok_session":
        return None
    if payload.get("login_method") not in ("sso", "username_password"):
        return None
    user_id = payload.get("user_id")
    return user_id if isinstance(user_id, str) and user_id else None

