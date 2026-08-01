
def raise_or_inc(value):
    if value.numel() == 2:
        raise ValueError("Expected error")
    return value + 1

