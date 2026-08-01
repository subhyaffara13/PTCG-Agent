
def _validate_no_invalid_chars(value: str, field_name: str) -> None:
    """Ensure value contains only printable ASCII without spaces or braces.

    This mirrors the constraints enforced by other Redis clients for values that
    will appear in CLIENT LIST / CLIENT INFO output.
    """

    for ch in value:
        # printable ASCII without space: '!' (0x21) to '~' (0x7E)
        if ord(ch) < 0x21 or ord(ch) > 0x7E or ch in _BRACES:
            raise ValueError(
                f"{field_name} must not contain spaces, newlines, non-printable characters, or braces"
            )

