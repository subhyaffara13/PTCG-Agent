
def reconstruct_model_name(
    model_name: str,
    custom_llm_provider: Optional[str],
    metadata: dict,
) -> str:
    """Reconstruct full model name with provider prefix for logging."""
    # Check if deployment model name from router metadata is available (has original prefix)
    deployment_model_name = metadata.get("deployment")
    if deployment_model_name and "/" in deployment_model_name:
        # Use the deployment model name which preserves the original provider prefix
        return deployment_model_name
    elif custom_llm_provider and model_name and "/" not in model_name:
        # Only add prefix for Bedrock (not for direct Anthropic API)
        # This ensures Bedrock models get the prefix while direct Anthropic models don't
        if custom_llm_provider == "bedrock":
            return f"{custom_llm_provider}/{model_name}"
    return model_name

