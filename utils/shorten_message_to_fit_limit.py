from typing import Optional

def shorten_message_to_fit_limit(
    message, tokens_needed, model: Optional[str], raise_error_on_max_limit: bool = False
):
    """
    Shorten a message to fit within a token limit by removing characters from the middle.

    Args:
        message: The message to shorten
        tokens_needed: The maximum number of tokens allowed
        model: The model being used (optional)
        raise_error_on_max_limit: If True, raises an error when max attempts reached. If False, returns final trimmed content.
    """

    # For OpenAI models, even blank messages cost 7 token,
    # and if the buffer is less than 3, the while loop will never end,
    # hence the value 10.
    if model is not None and "gpt" in model and tokens_needed <= 10:
        return message

    content = message["content"]
    attempts = 0

    verbose_logger.debug(f"content: {content}")

    while attempts < MAX_TOKEN_TRIMMING_ATTEMPTS:
        verbose_logger.debug(f"getting token count for message: {message}")
        total_tokens = get_token_count([message], model)
        verbose_logger.debug(
            f"total_tokens: {total_tokens}, tokens_needed: {tokens_needed}"
        )

        if total_tokens <= tokens_needed:
            break

        ratio = (tokens_needed) / total_tokens

        new_length = int(len(content) * ratio) - 1
        new_length = max(0, new_length)

        half_length = new_length // 2
        left_half = content[:half_length]
        right_half = content[-half_length:]

        trimmed_content = left_half + ".." + right_half
        message["content"] = trimmed_content
        verbose_logger.debug(f"trimmed_content: {trimmed_content}")
        content = trimmed_content
        attempts += 1

    if attempts >= MAX_TOKEN_TRIMMING_ATTEMPTS and raise_error_on_max_limit:
        raise Exception(
            f"Failed to trim message to fit within {tokens_needed} tokens after {MAX_TOKEN_TRIMMING_ATTEMPTS} attempts"
        )

    return message

