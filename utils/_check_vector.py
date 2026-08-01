
def _check_vector(other):
    if not isinstance(other, Vector):
        raise TypeError('A Vector must be supplied')
    return other

