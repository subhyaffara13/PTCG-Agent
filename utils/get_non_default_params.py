
def get_non_default_params(passed_params: dict) -> dict:
    # filter out those parameters that were passed with non-default values
    non_default_params = {
        k: v
        for k, v in passed_params.items()
        if (
            k != "model"
            and k != "custom_llm_provider"
            and k in DEFAULT_CHAT_COMPLETION_PARAM_VALUES
            and v != DEFAULT_CHAT_COMPLETION_PARAM_VALUES[k]
        )
    }

    return non_default_params

