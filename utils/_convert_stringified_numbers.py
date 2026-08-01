
def _convert_stringified_numbers(value):
    """Convert stringified numbers (including scientific notation) to appropriate numeric types."""
    if isinstance(value, str):
        try:
            # Try to convert to float first to handle scientific notation like "3e-07"
            if "e" in value.lower() or "." in value:
                return float(value)
            # Try to convert to int for whole numbers like "8192"
            else:
                return int(value)
        except (ValueError, TypeError):
            # If conversion fails, return the original string
            return value
    return value

