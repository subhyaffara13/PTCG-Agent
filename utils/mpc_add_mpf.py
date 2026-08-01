
def mpc_add_mpf(z, x, prec, rnd=round_fast):
    a, b = z
    return mpf_add(a, x, prec, rnd), b

