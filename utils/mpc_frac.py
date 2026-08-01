
def mpc_frac(z, prec, rnd=round_fast):
    a, b = z
    return mpf_frac(a, prec, rnd), mpf_frac(b, prec, rnd)

