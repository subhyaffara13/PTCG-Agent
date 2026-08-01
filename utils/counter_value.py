
def counter_value(name: str):
    """Return the value of the counter with the specified name"""
    return torch._C._lazy._counter_value(name)

