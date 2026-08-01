
def _none_or_positive_arg(x, name):
    if x is None:
        return -1
    if x < 0:
        raise ValueError(f"{name} must be >= 0")
    return x

