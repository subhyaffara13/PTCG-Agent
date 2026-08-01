
def strip_none_values_from_message(message: AllMessageValues) -> AllMessageValues:
    """
    Strips None values from message
    """
    return cast(AllMessageValues, {k: v for k, v in message.items() if v is not None})

