
def _normalize_native_redirect_uri(
    parsed,
) -> str:
    """Lowercase scheme, netloc, and path for allowlist comparison."""
    return urlunparse(
        (
            (parsed.scheme or "").lower(),
            (parsed.netloc or "").lower(),
            (parsed.path or "").lower(),
            "",
            "",
            "",
        )
    )

