
def get_standard_openai_params(params: dict) -> dict:
    return {
        k: v
        for k, v in params.items()
        if k in litellm.OPENAI_CHAT_COMPLETION_PARAMS and v is not None
    }

