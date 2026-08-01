
def _int_or_halfint(value):
    """return Python int unless value is half-int (then return float)"""
    if isinstance(value, int):
        return value
    elif type(value) is float:
        if value.is_integer():
            return int(value)  # an int
        if (2*value).is_integer():
            return value  # a float
    elif isinstance(value, Rational):
        if value.q == 2:
            return value.p/value.q  # a float
        elif value.q == 1:
            return value.p  # an int
    elif isinstance(value, Float):
        return _int_or_halfint(float(value))
    raise ValueError("expecting integer or half-integer, got %s" % value)

