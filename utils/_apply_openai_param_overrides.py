
def _apply_openai_param_overrides(
    optional_params: dict, non_default_params: dict, allowed_openai_params: list
):
    """
    If user passes in allowed_openai_params, apply them to optional_params

    These params will get passed as is to the LLM API since the user opted in to passing them in the request

    Only params the caller actually sent are forwarded. Previously this
    function unconditionally wrote `None` for any allowed param missing from
    the request, which then reached the provider SDK as a top-level kwarg it
    did not recognize (e.g. openai SDK raising
    `AsyncCompletions.create() got an unexpected keyword argument 'enable_thinking'`).
    See https://github.com/BerriAI/litellm/issues/25697
    """
    if allowed_openai_params:
        for param in allowed_openai_params:
            if param in optional_params:
                continue
            if param not in non_default_params:
                continue
            optional_params[param] = non_default_params.pop(param)
    return optional_params

