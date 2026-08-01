
def get_litellm_logging_class() -> Type["Logging"]:
    """Get the cached LiteLLM Logging class, initializing if needed."""
    global _LiteLLMLogging
    if _LiteLLMLogging is not None:
        return _LiteLLMLogging
    from litellm.litellm_core_utils.litellm_logging import Logging

    _LiteLLMLogging = Logging
    return _LiteLLMLogging

