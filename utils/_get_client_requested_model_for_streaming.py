
def _get_client_requested_model_for_streaming(request_data: dict) -> str:
    """
    Prefer the original client-requested model (pre-alias mapping) when available.

    Pre-call processing can rewrite `request_data["model"]` for aliasing/routing purposes.
    The OpenAI-compatible public `model` field should reflect what the client sent.
    """
    requested_model = request_data.get("_litellm_client_requested_model")
    if isinstance(requested_model, str):
        return requested_model

    requested_model = request_data.get("model")
    return requested_model if isinstance(requested_model, str) else ""

