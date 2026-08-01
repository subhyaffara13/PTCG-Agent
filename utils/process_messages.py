
def process_messages(messages, max_tokens, model):
    # Process messages from older to more recent
    messages = messages[::-1]
    final_messages = []
    verbose_logger.debug(
        f"calling process_messages with messages: {messages}, max_tokens: {max_tokens}, model: {model}"
    )
    for message in messages:
        verbose_logger.debug(f"processing final_messages: {final_messages}")
        used_tokens = get_token_count(final_messages, model)
        available_tokens = max_tokens - used_tokens
        verbose_logger.debug(
            f"used_tokens: {used_tokens}, available_tokens: {available_tokens}"
        )
        if available_tokens <= 3:
            break

        final_messages = attempt_message_addition(
            final_messages=final_messages,
            message=message,
            available_tokens=available_tokens,
            max_tokens=max_tokens,
            model=model,
        )
        verbose_logger.debug(
            f"final_messages after attempt_message_addition: {final_messages}"
        )
    verbose_logger.debug(f"Final messages: {final_messages}")
    return final_messages

