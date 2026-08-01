
def quote_type_string(type_string: str) -> str:
    """Quotes a type representation for use in messages."""
    if (
        type_string in ["Module", "overloaded function", "<deleted>"]
        or type_string.startswith("Module ")
        or type_string.endswith("?")
    ):
        # These messages are easier to read if these aren't quoted.
        return type_string
    return f'"{type_string}"'

