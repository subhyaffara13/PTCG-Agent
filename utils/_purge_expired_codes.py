import time

def _purge_expired_codes() -> None:
    now = time.time()
    expired = [k for k, v in _byok_auth_codes.items() if v["expires_at"] < now]
    for k in expired:
        del _byok_auth_codes[k]

