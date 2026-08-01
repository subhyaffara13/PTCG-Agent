
def _forward_kwargs(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if k not in _LITELLM_INTERNAL_KWARGS}

