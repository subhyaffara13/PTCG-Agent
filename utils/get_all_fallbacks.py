
def get_all_fallbacks(
    model: str,
    llm_router: Optional[Router] = None,
    fallback_type: str = "general",
) -> List[str]:
    """
    Get all fallbacks for a given model from the router's fallback configuration.

    Args:
        model: The model name to get fallbacks for
        llm_router: The LiteLLM router instance
        fallback_type: Type of fallback ("general", "context_window", "content_policy")

    Returns:
        List of fallback model names. Empty list if no fallbacks found.
    """
    if llm_router is None:
        return []

    # Get the appropriate fallback list based on type
    fallbacks_config: list = []
    if fallback_type == "general":
        fallbacks_config = getattr(llm_router, "fallbacks", [])
    elif fallback_type == "context_window":
        fallbacks_config = getattr(llm_router, "context_window_fallbacks", [])
    elif fallback_type == "content_policy":
        fallbacks_config = getattr(llm_router, "content_policy_fallbacks", [])
    else:
        verbose_proxy_logger.warning(f"Unknown fallback_type: {fallback_type}")
        return []

    if not fallbacks_config:
        return []

    try:
        # Use existing function to get fallback model group
        fallback_model_group, _ = get_fallback_model_group(
            fallbacks=fallbacks_config, model_group=model
        )

        if fallback_model_group is None:
            return []

        return fallback_model_group
    except Exception as e:
        verbose_proxy_logger.error(f"Error getting fallbacks for model {model}: {e}")
        return []

