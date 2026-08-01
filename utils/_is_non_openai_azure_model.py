
def _is_non_openai_azure_model(model: str) -> bool:
    try:
        model_name = model.split("/", 1)[1]
        if (
            model_name in litellm.cohere_chat_models
            or f"mistral/{model_name}" in litellm.mistral_chat_models
        ):
            return True
    except Exception:
        return False
    return False

