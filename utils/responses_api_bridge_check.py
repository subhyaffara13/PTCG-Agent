from typing import Any, Dict, List, Optional, Tuple

def responses_api_bridge_check(
    model: str,
    custom_llm_provider: str,
    web_search_options: Optional[OpenAIWebSearchOptions] = None,
    tools: Optional[List[Any]] = None,
    reasoning_effort: Optional[Any] = None,
    reasoning_summary: Optional[Any] = None,
) -> Tuple[dict, str]:
    model_info: Dict[str, Any] = {}

    # Global flag: route ALL OpenAI chat completions through Responses API.
    # Returns early with minimal model_info; callers only inspect the "mode" key.
    if litellm.route_all_chat_openai_to_responses and custom_llm_provider == "openai":
        model = model.replace("responses/", "")
        model_info["mode"] = "responses"
        return model_info, model

    try:
        model_info = cast(
            dict,
            _get_model_info_helper(
                model=model, custom_llm_provider=custom_llm_provider
            ),
        )
        if model_info.get("mode") is None and model.startswith("responses/"):
            model = model.replace("responses/", "")
            mode = "responses"
            model_info["mode"] = mode

        if web_search_options is not None and custom_llm_provider == "xai":
            model_info["mode"] = "responses"
            model = model.replace("responses/", "")

    except Exception as e:
        verbose_logger.debug("Error getting model info: {}".format(e))

        if model.startswith(
            "responses/"
        ):  # handle azure models - `azure/responses/<deployment-name>`
            model = model.replace("responses/", "")
            mode = "responses"
            model_info["mode"] = mode

    # OpenAI/Azure GPT-5 chat-completions that need Responses-only fields (e.g.
    # ``reasoningSummary`` in ``extra_body``) must be bridged; Chat Completions rejects
    # those keys.
    #
    # - gpt-5.4+: tools + reasoning_effort (original) or any reasoning-summary alias.
    # - Older GPT-5 names (e.g. ``gpt-5``, ``gpt-5.1``): bridge only when a reasoning
    #   summary alias is present with ``reasoning_effort`` (tools alone stay on chat).
    if (
        custom_llm_provider in ("openai", "azure")
        and model_info.get("mode") != "responses"
        and OpenAIGPT5Config.is_model_gpt_5_model(model)
        and not OpenAIGPT5Config.is_model_gpt_5_search_model(model)
        and reasoning_effort is not None
        and (
            reasoning_summary is not None
            or (OpenAIGPT5Config.is_model_gpt_5_4_plus_model(model) and tools)
        )
    ):
        model_info["mode"] = "responses"
        model = model.replace("responses/", "")

    return model_info, model

