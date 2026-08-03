import re

def mpc_log(z, prec, rnd=round_fast):
    re = mpf_log_hypot(z[0], z[1], prec, rnd)
    im = mpc_arg(z, prec, rnd)
    return re, im

