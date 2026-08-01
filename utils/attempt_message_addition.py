
def attempt_message_addition(
    final_messages, message, available_tokens, max_tokens, model
):
    temp_messages = [message] + final_messages
    temp_message_tokens = get_token_count(messages=temp_messages, model=model)
    verbose_logger.debug(
        f"temp_message_tokens: {temp_message_tokens}, max_tokens: {max_tokens}"
    )
    if temp_message_tokens <= max_tokens:
        return temp_messages

    # if temp_message_tokens > max_tokens, try shortening temp_messages
    elif "function_call" not in message:
        verbose_logger.debug("attempting to shorten message to fit limit")
        # fit updated_message to be within temp_message_tokens - max_tokens (aka the amount temp_message_tokens is greate than max_tokens)
        updated_message = shorten_message_to_fit_limit(message, available_tokens, model)
        if can_add_message(updated_message, final_messages, max_tokens, model):
            verbose_logger.debug(
                "can add message, returning [updated_message] + final_messages"
            )
            return [updated_message] + final_messages
        else:
            verbose_logger.debug("cannot add message, returning final_messages")
    return final_messages

