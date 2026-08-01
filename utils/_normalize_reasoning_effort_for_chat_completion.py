
def _normalize_reasoning_effort_for_chat_completion(
    value: Union[str, dict, None],
) -> Optional[str]:
    """Convert reasoning_effort to the string format expected by OpenAI chat completion API.

    The chat completion API expects a simple string: 'none', 'low', 'medium', 'high', or 'xhigh'.
    Config/deployments may pass the Responses API format: {'effort': 'high', 'summary': 'detailed'}.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and "effort" in value:
        return value["effort"]
    return None

