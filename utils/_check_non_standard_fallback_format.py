
def _check_non_standard_fallback_format(fallbacks: Optional[List[Any]]) -> bool:
    """
    Checks if the fallbacks list is a list of strings or a list of dictionaries.

    If
    - List[str]: e.g. ["claude-3-haiku", "openai/o-1"]
    - List[Dict[<LiteLLMParamsTypedDict>, Any]]: e.g. [{"model": "claude-3-haiku", "messages": [{"role": "user", "content": "Hey, how's it going?"}]}]

    If [{"gpt-3.5-turbo": ["claude-3-haiku"]}] then standard format.
    """
    if fallbacks is None or not isinstance(fallbacks, list) or len(fallbacks) == 0:
        return False
    if all(isinstance(item, str) for item in fallbacks):
        return True
    elif all(isinstance(item, dict) for item in fallbacks):
        for item in fallbacks:
            for key in LiteLLMParamsTypedDict.__annotations__.keys():
                if key in item:
                    # If the value is a list, it's likely a standard fallback model group mapping
                    # (e.g. {"model": ["backup"]}) rather than a parameter override.
                    if not isinstance(item[key], list):
                        return True

    return False

