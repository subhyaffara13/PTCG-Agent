import os
import time

def _get_token_from_oidc() -> str | None:
    """Get a short-lived OIDC token in CI (Trusted Publishers).

    Enabled by setting `HF_OIDC_RESOURCE`, which scopes the token to a repo or user.
    The ID token is read from `HF_OIDC_ID_TOKEN` if available, or minted from a supported CI provider (e.g. GitHub Actions).

    Returns `None` when OIDC is not enabled.
    If enabled, any failure is raised explicitly rather than falling back silently.

    See `huggingface_hub._oidc` and https://huggingface.co/docs/hub/trusted-publishers.
    """
    resource = os.environ.get("HF_OIDC_RESOURCE")
    if not resource:
        return None

    from .._oidc import detect_provider, oidc_login

    global _OIDC_TOKEN_CACHE
    with _OIDC_TOKEN_LOCK:
        now = time.monotonic()
        if (
            _OIDC_TOKEN_CACHE is not None
            and _OIDC_TOKEN_CACHE["resource"] == resource
            and now < _OIDC_TOKEN_CACHE["expires_at"]
        ):
            return _OIDC_TOKEN_CACHE["token"]

        # An explicit id token (any provider) takes precedence; otherwise mint from a detected one.
        subject_token = os.environ.get("HF_OIDC_ID_TOKEN") or None
        if subject_token is None and detect_provider() is None:
            raise OIDCError(
                "HF_OIDC_RESOURCE is set but no OIDC id token is available: not running in a supported "
                "CI provider (github) and HF_OIDC_ID_TOKEN is not set. Set HF_OIDC_ID_TOKEN to the id "
                "token minted by your CI provider, or unset HF_OIDC_RESOURCE."
            )

        result = oidc_login(resource=resource, subject_token=subject_token)
        token = result["access_token"]
        expires_in = int(result.get("expires_in", 3600))
        # A pre-supplied HF_OIDC_ID_TOKEN can't be re-minted, so refreshing early is pointless (the id
        # token is likely already expired by then): cache for the full lifetime. Only the auto-minted
        # path can refresh, so only it gets the safety margin.
        margin = 0 if subject_token is not None else _OIDC_REFRESH_MARGIN
        _OIDC_TOKEN_CACHE = {
            "resource": resource,
            "token": token,
            "expires_at": now + max(expires_in - margin, 0),
        }
        return token

