import re

def mpc_mul_int(z, n, prec, rnd=round_fast):
    a, b = z
    re = mpf_mul_int(a, n, prec, rnd)
    im = mpf_mul_int(b, n, prec, rnd)
    return re, im

