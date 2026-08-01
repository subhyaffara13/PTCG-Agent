
def mpc_floor(z, prec, rnd=round_fast):
    a, b = z
    return mpf_floor(a, prec, rnd), mpf_floor(b, prec, rnd)

