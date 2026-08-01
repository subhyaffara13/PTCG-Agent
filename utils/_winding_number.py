
def _winding_number(T, field):
    """Compute the winding number of the input polynomial, i.e. the number of roots. """
    return int(sum(field(*_values[t][i]) for t, i in T) / field(2))

