
def _extract_file_access_credentials(litellm_params: Optional[dict]) -> dict:
    """
    Extract credentials from litellm_params for file access operations.

    This method extracts relevant authentication and configuration parameters
    needed for accessing files across different providers (Azure, Vertex AI, etc.).

    Args:
        litellm_params: Dictionary containing litellm parameters with credentials

    Returns:
        Dictionary containing only the credentials needed for file access
    """
    credentials = {}

    if litellm_params:
        # List of credential keys that should be passed to file operations
        credential_keys = [
            "api_key",
            "api_base",
            "api_version",
            "organization",
            "azure_ad_token",
            "azure_ad_token_provider",
            "vertex_project",
            "vertex_location",
            "vertex_credentials",
            "timeout",
            "max_retries",
        ]
        for key in credential_keys:
            if key in litellm_params:
                credentials[key] = litellm_params[key]

    return credentials

