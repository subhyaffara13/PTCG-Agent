
def resolve_provider(custom_llm_provider: str | None) -> str:
    """Map a litellm provider string to a ``gen_ai.provider.name`` value.

    Unknown providers pass through verbatim — the convention explicitly allows
    provider-specific values, so an unmapped name is still valid.
    """
    if not custom_llm_provider:
        return ""
    mapped = _PROVIDER_BY_LITELLM.get(custom_llm_provider.lower())
    return mapped.value if mapped is not None else custom_llm_provider

