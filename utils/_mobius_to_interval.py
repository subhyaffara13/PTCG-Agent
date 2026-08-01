
def _mobius_to_interval(M, field):
    """Convert a Mobius transform to an open interval. """
    a, b, c, d = M

    s, t = field(a, c), field(b, d)

    if s <= t:
        return (s, t)
    else:
        return (t, s)

