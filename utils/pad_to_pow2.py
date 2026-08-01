
def pad_to_pow2(value: int, max_value: int, min_value: int = 0) -> int:
    """Return the smallest power of 2 >= (value), capped at (max_value). If a minimum value is provided, the value is at
    least padded to that value."""
    value = max(value, max(1, min_value))
    padded = 2 ** int(ceil(log2(value)))
    return min(padded, max_value)

