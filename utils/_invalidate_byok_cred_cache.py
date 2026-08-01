
def _invalidate_byok_cred_cache(user_id: str, server_id: str) -> None:
    """Remove a (user_id, server_id) entry from the BYOK credential cache.

    Call this after storing or deleting a credential so subsequent calls
    see the fresh value rather than a stale cached result.
    """
    _byok_cred_cache.pop((user_id, server_id), None)

