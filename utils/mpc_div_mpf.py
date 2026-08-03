import re

def mpc_div_mpf(z, p, prec, rnd=round_fast):
    """Calculate z/p where p is real"""
    a, b = z
    re = mpf_div(a, p, prec, rnd)
    im = mpf_div(b, p, prec, rnd)
    return re, im

