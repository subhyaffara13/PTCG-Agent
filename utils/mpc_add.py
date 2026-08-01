
def mpc_add(z, w, prec, rnd=round_fast):
    a, b = z
    c, d = w
    return mpf_add(a, c, prec, rnd), mpf_add(b, d, prec, rnd)

