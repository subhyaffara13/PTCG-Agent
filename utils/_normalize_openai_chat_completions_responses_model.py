
def _normalize_openai_chat_completions_responses_model(model: str) -> tuple[str, bool]:
    """
    Strip `openai/chat_completions/<name>` → `openai/<name>` and return True when the
    prefix was applied (same effect as use_chat_completions_api=True).
    """
    if not model.startswith(_OPENAI_CHAT_COMPLETIONS_RESPONSES_MODEL_PREFIX):
        return model, False
    remainder = model[len(_OPENAI_CHAT_COMPLETIONS_RESPONSES_MODEL_PREFIX) :]
    if not remainder:
        return model, False
    return f"openai/{remainder}", True

