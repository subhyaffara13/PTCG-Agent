
def mpc_sub_mpf(z, p, prec=0, rnd=round_fast):
    a, b = z
    return mpf_sub(a, p, prec, rnd), b

