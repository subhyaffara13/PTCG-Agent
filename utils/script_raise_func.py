
def script_raise_func(value):
    if value.numel() == 2:
        raise ValueError("Expected error")
    return value + 1

