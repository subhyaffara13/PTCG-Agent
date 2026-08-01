
def positive_any_number(value: int | float | None = None):
    if value is not None and (not isinstance(value, (int, float)) or not value >= 0):
        raise ValueError(f"Value must be a positive integer or floating number, got {value}")

