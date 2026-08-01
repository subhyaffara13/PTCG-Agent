
def github_copilot_supports_responses_api(model: str) -> bool:
    """
    Gate native /v1/responses dispatch per github_copilot model.

    Resolution (first match wins): mode "responses" -> True; mode "chat" ->
    False (opt-out wins for dual-endpoint models); "/v1/responses" in
    supported_endpoints -> True; else False. Unknown model -> False (the bridge
    always works since every Copilot model supports /chat/completions).

    Reads merged model info (per-deployment model_info applied via the router's
    register_model, which also clears the cache used here).
    """
    try:
        info = _cached_get_model_info_helper(
            model=model, custom_llm_provider="github_copilot"
        )
    except Exception as e:
        verbose_logger.debug(
            "github_copilot_supports_responses_api: get_model_info failed "
            "for %s: %s",
            model,
            e,
        )
        return False

    mode = info.get("mode")
    if mode == "responses":
        return True
    if mode == "chat":
        return False

    # supported_endpoints is dropped by ModelInfoBase; read it from the raw
    # model_cost entry via the resolved key.
    key = info.get("key")
    raw_info = litellm.model_cost.get(key) if isinstance(key, str) else None
    endpoints = (
        raw_info.get("supported_endpoints") if isinstance(raw_info, dict) else None
    )
    return isinstance(endpoints, list) and "/v1/responses" in endpoints

