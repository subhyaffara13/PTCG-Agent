
def _pop_use_chat_completions_api_kw(kwargs: Dict[str, Any]) -> bool:
    """Pop use_chat_completions_api; True when the chat-completions bridge is requested."""
    use_cc = kwargs.pop("use_chat_completions_api", None)
    return bool(use_cc)

