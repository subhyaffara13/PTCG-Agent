
def mpc_pos(z, prec, rnd=round_fast):
    a, b = z
    return mpf_pos(a, prec, rnd), mpf_pos(b, prec, rnd)

