
def mpc_abs(z, prec, rnd=round_fast):
    """Absolute value of a complex number, |a+bi|.
    Returns an mpf value."""
    a, b = z
    return mpf_hypot(a, b, prec, rnd)

