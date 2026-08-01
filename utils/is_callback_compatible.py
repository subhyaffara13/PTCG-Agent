
def is_callback_compatible(callback_name: str) -> bool:
    """
    Check if a callback_name exists in the compatible callbacks list

    Args:
        callback_name: Name of the callback to check

    Returns:
        bool: True if callback_name exists in the compatible callbacks, False otherwise
    """
    compatible_callbacks = load_compatible_callbacks()
    return callback_name in compatible_callbacks

