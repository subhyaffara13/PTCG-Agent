
def mpc_arg(z, prec, rnd=round_fast):
    """Argument of a complex number. Returns an mpf value."""
    a, b = z
    return mpf_atan2(b, a, prec, rnd)

