import re

def mpc_ellipk(z, prec, rnd=round_fast):
    re, im = z
    if im == fzero:
        if re == finf:
            return mpc_zero
        if mpf_le(re, fone):
            return mpf_ellipk(re, prec, rnd), fzero
    wp = prec + 15
    a = mpc_sqrt(mpc_sub(mpc_one, z, wp), wp)
    v = mpc_agm1(a, wp)
    r = mpc_mpf_div(mpf_pi(wp), v, prec, rnd)
    return mpc_shift(r, -1)

