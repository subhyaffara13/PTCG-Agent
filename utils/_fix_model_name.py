
def _fix_model_name(model: str) -> str:
    """We normalize some model names to others"""
    if model in litellm.azure_llms:
        # azure llms use gpt-35-turbo instead of gpt-3.5-turbo 🙃
        return model.replace("-35", "-3.5")
    elif model in litellm.open_ai_chat_completion_models:
        return model  # type: ignore
    else:
        return "gpt-3.5-turbo"

