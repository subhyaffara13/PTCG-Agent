
def _validate_length(values, expected, name):
    if len(values) != expected:
        raise ValueError(f"{name} must match the number of inputs")

