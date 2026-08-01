
def get_openai_credentials(
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
) -> OpenAICredentials:
    """Resolve OpenAI credentials from params, litellm globals, and env vars."""
    resolved_api_base = (
        api_base
        or litellm.api_base
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("OPENAI_API_BASE")
        or "https://api.openai.com/v1"
    )
    resolved_organization = (
        organization
        or litellm.organization
        or os.getenv("OPENAI_ORGANIZATION", None)
        or None
    )
    resolved_api_key = (
        api_key or litellm.api_key or litellm.openai_key or os.getenv("OPENAI_API_KEY")
    )
    return OpenAICredentials(
        api_base=resolved_api_base,
        api_key=resolved_api_key,
        organization=resolved_organization,
    )

