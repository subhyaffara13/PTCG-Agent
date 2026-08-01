
def feq(a, b, max_relative_error=1e-12, max_absolute_error=1e-12):
    a = float(a)
    b = float(b)
    # if the numbers are close enough (absolutely), then they are equal
    if abs(a - b) < max_absolute_error:
        return True
    # if not, they can still be equal if their relative error is small
    if abs(b) > abs(a):
        relative_error = abs((a - b)/b)
    else:
        relative_error = abs((a - b)/a)
    return relative_error <= max_relative_error


def feq(a, b):
    """Test if two floating point values are 'equal'."""
    t_float = Float("1.0E-10")
    return -t_float < a - b < t_float


def feq(a, b):
    """Test if two floating point values are 'equal'."""
    t_float = Float("1.0E-10")
    return -t_float < a - b < t_float

