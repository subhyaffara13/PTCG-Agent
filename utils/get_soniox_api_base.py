from typing import Optional

def get_soniox_api_base(api_base: Optional[str] = None) -> str:
    """Resolve the Soniox API base URL from arg or env var (defaults to public API)."""
    from litellm.secret_managers.main import get_secret_str

    base = api_base or get_secret_str("SONIOX_API_BASE") or SONIOX_API_BASE
    return base.rstrip("/")

