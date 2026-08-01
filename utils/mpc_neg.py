
def mpc_neg(z, prec=None, rnd=round_fast):
    a, b = z
    return mpf_neg(a, prec, rnd), mpf_neg(b, prec, rnd)

