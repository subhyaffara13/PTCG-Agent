
def mantle_supports_responses(model: str | None, model_cost: dict) -> bool:
    """Whether a Bedrock Mantle model can serve the native Responses API.

    Purely data-driven from the model's price-map capability signal -- either
    /v1/responses in supported_endpoints, or mode=responses -- both overridable
    via register_model and proxy model_info, so onboarding a model is a JSON
    change, never a code change. There is deliberately NO model-name match here:
    capability is per-model, not per-family (openai.gpt-oss-120b supports
    Responses while openai.gpt-oss-safeguard-120b does not, despite sharing the
    gpt-oss substring), so a substring gate would be wrong. A model absent from
    model_cost simply has no signal and returns False (chat-completions emulation).
    """
    entry = model_cost.get(f"bedrock_mantle/{model}", {})
    if "/v1/responses" in (entry.get("supported_endpoints") or []):
        return True
    return entry.get("mode") == "responses"

