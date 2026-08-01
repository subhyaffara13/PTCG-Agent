
def is_cloudzero_setup_in_config() -> bool:
    """
    Check if CloudZero is setup in config.yaml or environment variables.

    CloudZero is considered setup in config if:
    - "cloudzero" is in the callbacks list in config.yaml, OR
    Returns:
        bool: True if CloudZero is configured, False otherwise
    """
    import litellm

    return "cloudzero" in litellm.callbacks

