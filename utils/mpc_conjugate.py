
def mpc_conjugate(z, prec, rnd=round_fast):
    re, im = z
    return re, mpf_neg(im, prec, rnd)

