
def mpc_ceil(z, prec, rnd=round_fast):
    a, b = z
    return mpf_ceil(a, prec, rnd), mpf_ceil(b, prec, rnd)

