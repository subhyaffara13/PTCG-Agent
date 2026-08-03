from typing import Optional

def get_azure_credentials(
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: Optional[str] = None,
) -> AzureCredentials:
    """Resolve Azure credentials from params, litellm globals, and env vars."""
    resolved_api_base = api_base or litellm.api_base or get_secret_str("AZURE_API_BASE")
    resolved_api_version = (
        api_version or litellm.api_version or get_secret_str("AZURE_API_VERSION")
    )
    resolved_api_key = (
        api_key
        or litellm.api_key
        or litellm.azure_key
        or get_secret_str("AZURE_OPENAI_API_KEY")
        or get_secret_str("AZURE_API_KEY")
    )
    return AzureCredentials(
        api_base=resolved_api_base,
        api_key=resolved_api_key,
        api_version=resolved_api_version,
    )

