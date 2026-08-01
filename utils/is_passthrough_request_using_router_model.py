
def is_passthrough_request_using_router_model(
    request_body: dict, llm_router: Optional[litellm.Router]
) -> bool:
    """
    Returns True if the model is in the llm_router model names
    """
    try:
        model = request_body.get("model")
        return is_known_model(model, llm_router)
    except Exception:
        return False

