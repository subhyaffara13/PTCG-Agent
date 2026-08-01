
def _accepts_litellm_call_info(cb: CustomLogger) -> bool:
    key = id(type(cb))
    if key not in _CALLBACK_ACCEPTS_CALL_INFO:
        sig = inspect.signature(cb.async_post_call_response_headers_hook)
        _CALLBACK_ACCEPTS_CALL_INFO[key] = "litellm_call_info" in sig.parameters
    return _CALLBACK_ACCEPTS_CALL_INFO[key]

