
def mpc_cosh(z, prec, rnd=round_fast):
    """Complex hyperbolic cosine. Computed as cosh(z) = cos(z*i)."""
    a, b = z
    return mpc_cos((b, mpf_neg(a)), prec, rnd)

