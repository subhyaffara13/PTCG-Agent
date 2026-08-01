
def mpc_asinh(z, prec, rnd=round_fast):
    # asinh(z) = I * asin(-I z)
    a, b = z
    a, b =  mpc_asin((b, mpf_neg(a)), prec, rnd)
    return mpf_neg(b), a

