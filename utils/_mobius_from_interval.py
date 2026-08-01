
def _mobius_from_interval(I, field):
    """Convert an open interval to a Mobius transform. """
    s, t = I

    a, c = field.numer(s), field.denom(s)
    b, d = field.numer(t), field.denom(t)

    return a, b, c, d

