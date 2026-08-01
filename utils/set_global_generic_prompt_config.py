
def set_global_generic_prompt_config(config: dict) -> None:
    """
    Set the global generic prompt configuration.

    Args:
        config: Dictionary containing generic prompt configuration
                - api_base: Base URL for the API
                - api_key: Optional API key for authentication
                - timeout: Request timeout in seconds (default: 30)
    """
    import litellm

    litellm.global_generic_prompt_config = config  # type: ignore

