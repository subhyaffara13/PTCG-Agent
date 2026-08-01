
def mpc_cbrt(z, prec, rnd=round_fast):
    """
    Complex cubic root.
    """
    return mpc_nthroot(z, 3, prec, rnd)

