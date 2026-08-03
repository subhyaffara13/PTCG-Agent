from typing import Optional

def scope_session_to_principal(session_id: str, principal: Optional[str]) -> str:
    """
    Bind a client-supplied A2A contextId to the authenticated principal.

    Without this, two distinct keys authorized for the same LangFlow agent could
    set the same contextId and read/append to each other's LangFlow memory. The
    principal is hashed (it is already a hashed token) so the raw value is never
    sent to the LangFlow backend, while the original contextId is kept as a
    suffix for operator-side correlation.
    """
    if not principal:
        return session_id
    principal_prefix = hashlib.sha256(principal.encode("utf-8")).hexdigest()[:16]
    return f"{principal_prefix}-{session_id}"

