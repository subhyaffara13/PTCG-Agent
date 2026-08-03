from typing import Optional

def get_soniox_api_key(api_key: Optional[str] = None) -> Optional[str]:
    """Resolve the Soniox API key from arg or env var."""
    # Local import to avoid a circular import: litellm.secret_managers.main
    # imports from litellm at top-level.
    from litellm.secret_managers.main import get_secret_str

    return api_key or get_secret_str("SONIOX_API_KEY")

