
def _transcription_usage_has_token_details(
    usage_block: Optional[Usage],
) -> bool:
    if usage_block is None:
        return False

    prompt_tokens_val = getattr(usage_block, "prompt_tokens", 0) or 0
    completion_tokens_val = getattr(usage_block, "completion_tokens", 0) or 0
    prompt_details = getattr(usage_block, "prompt_tokens_details", None)

    if prompt_details is not None:
        audio_token_count = getattr(prompt_details, "audio_tokens", 0) or 0
        text_token_count = getattr(prompt_details, "text_tokens", 0) or 0
        if audio_token_count > 0 or text_token_count > 0:
            return True

    return (prompt_tokens_val > 0) or (completion_tokens_val > 0)

