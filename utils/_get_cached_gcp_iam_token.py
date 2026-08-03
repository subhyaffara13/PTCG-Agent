import time

def _get_cached_gcp_iam_token(service_account: str) -> str:
    """
    Return a cached GCP IAM token, refreshing only when expired.

    Uses a module-level cache shared across all GCPIAMCredentialProvider
    instances for the same service account. The threading.Lock ensures only
    one thread performs the network round-trip on expiry; all others wait
    briefly and read the fresh token (double-checked locking pattern).

    This avoids N concurrent blocking IAM refreshes when N Redis connections
    are established simultaneously (e.g. during health checks or pool warm-up),
    which would otherwise serialise inside Python's async event loop and cause
    cascading request latency.
    """
    cached = _token_cache.get(service_account)
    if cached is not None:
        token, expiry = cached
        if time.monotonic() < expiry:
            return token

    with _token_cache_lock:
        # Re-check inside the lock: another thread may have refreshed already.
        cached = _token_cache.get(service_account)
        if cached is not None:
            token, expiry = cached
            if time.monotonic() < expiry:
                return token

        token = _generate_gcp_iam_access_token(service_account)
        _token_cache[service_account] = (
            token,
            time.monotonic() + _GCP_IAM_TOKEN_TTL_SECONDS,
        )
        return token

