
def cleanup_none_field_in_message(message: AllMessageValues):
    """
    Cleans up the message by removing the none field.

    remove None fields in the message - e.g. {"function": None} - some providers raise validation errors
    """
    new_message = message.copy()
    return {k: v for k, v in new_message.items() if v is not None}

