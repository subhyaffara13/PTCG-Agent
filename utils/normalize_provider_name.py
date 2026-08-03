from typing import Optional

def normalize_provider_name(provider: Optional[str]) -> Optional[str]:
    """
    Normalize LiteLLM provider names to standardized string names.

    Args:
        provider: LiteLLM internal provider name

    Returns:
        Normalized provider name or the original if no mapping exists
    """
    if provider is None:
        return None

    # Provider mapping to names used in Opik
    provider_mapping = {
        "openai": "openai",
        "vertex_ai-language-models": "google_vertexai",
        "gemini": "google_ai",
        "anthropic": "anthropic",
        "vertex_ai-anthropic_models": "anthropic_vertexai",
        "bedrock": "bedrock",
        "bedrock_converse": "bedrock",
        "groq": "groq",
    }

    return provider_mapping.get(provider, provider)

