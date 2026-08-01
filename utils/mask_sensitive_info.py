
def mask_sensitive_info(error_message):
    # Find the start of the key parameter
    if isinstance(error_message, str):
        key_index = error_message.find("key=")
    else:
        return error_message

    # If key is found
    if key_index != -1:
        # Find the end of the key parameter (next & or end of string)
        next_param = error_message.find("&", key_index)

        if next_param == -1:
            # If no more parameters, mask until the end of the string
            masked_message = error_message[: key_index + 4] + "[REDACTED_API_KEY]"
        else:
            # Replace the key with redacted value, keeping other parameters
            masked_message = (
                error_message[: key_index + 4]
                + "[REDACTED_API_KEY]"
                + error_message[next_param:]
            )

        return masked_message

    return error_message

