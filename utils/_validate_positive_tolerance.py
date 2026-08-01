
def _validate_positive_tolerance(value, name):
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _validate_positive_tolerance(max_err):
    if max_err <= 0:
        raise ValueError("max_err must be greater than zero")

