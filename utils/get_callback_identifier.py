
def get_callback_identifier(callback):
    """
    Get the callback identifier string, handling both strings and objects.

    This function extracts a string identifier from a callback, which can be:
    - A string (returned as-is)
    - An object with a callback_name attribute
    - An object registered in CustomLoggerRegistry
    - Falls back to callback_name() helper function

    Args:
        callback: The callback to identify (can be str or object)

    Returns:
        str: The callback identifier string
    """
    if isinstance(callback, str):
        return callback
    if hasattr(callback, "callback_name") and callback.callback_name:
        return callback.callback_name
    if hasattr(callback, "__class__"):
        callback_strs = CustomLoggerRegistry.get_all_callback_strs_from_class_type(
            callback.__class__
        )
        if (
            hasattr(callback, "callback_name")
            and callback.callback_name in callback_strs
        ):
            return callback.callback_name
        if callback_strs:
            return callback_strs[0]
    return callback_name(callback)

