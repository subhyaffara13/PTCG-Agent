
def get_non_default_completion_params(kwargs: dict) -> dict:
    openai_params = litellm.OPENAI_CHAT_COMPLETION_PARAMS
    default_params = openai_params + all_litellm_params
    non_default_params = {
        k: v for k, v in kwargs.items() if k not in default_params
    }  # model-specific params - pass them straight to the model/provider

    return non_default_params

