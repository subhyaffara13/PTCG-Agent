
def _gettext_noop(message: str) -> str:
    """Mark a string as a translation string without translating it.

    Example usage:
    ```python
    CONSTANTS = [_gettext_noop('first'), _gettext_noop('second')]
    def num_name(n):
        return _gettext(CONSTANTS[n])
    ```

    Args:
        message (str): Text to translate in the future.

    Returns:
        str: Original text, unchanged.
    """
    return message

