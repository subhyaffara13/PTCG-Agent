
def _model_uses_max_completion_tokens(model: str) -> bool:
    """Return True for OCI-hosted models that require ``maxCompletionTokens``.

    OpenAI commercial models proxied through OCI (``openai.*``) reject
    ``maxTokens`` with HTTP 400 on the reasoning families (gpt-5.x, o-series)
    and accept ``maxCompletionTokens`` everywhere, so route the whole vendor
    prefix to it rather than chasing each new release in
    ``model_prices_and_context_window.json``. The ``openai.gpt-oss-*`` open
    weights are served by OCI's own stack and keep ``maxTokens``. Any other
    vendor falls back to the catalog's ``supports_reasoning`` flag.
    """
    if not model:
        return False
    name = model[4:] if model.lower().startswith("oci/") else model
    lowered = name.lower()
    if lowered.startswith("openai."):
        return not lowered.startswith("openai.gpt-oss")
    return supports_reasoning(model=name, custom_llm_provider="oci")

