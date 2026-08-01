
def positive_int(value: int | None = None):
    if value is not None and (not isinstance(value, int) or not value >= 0):
        raise ValueError(f"Value must be a positive integer, got {value}")

