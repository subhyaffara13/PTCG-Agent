import re

def mpc_nthroot(z, n, prec, rnd=round_fast):
    """
    Complex n-th root.

    Use Newton method as in the real case when it is faster,
    otherwise use z**(1/n)
    """
    a, b = z
    if a[0] == 0 and b == fzero:
        re = mpf_nthroot(a, n, prec, rnd)
        return (re, fzero)
    if n < 2:
        if n == 0:
            return mpc_one
        if n == 1:
            return mpc_pos((a, b), prec, rnd)
        if n == -1:
            return mpc_div(mpc_one, (a, b), prec, rnd)
        inverse = mpc_nthroot((a, b), -n, prec+5, reciprocal_rnd[rnd])
        return mpc_div(mpc_one, inverse, prec, rnd)
    if n <= 20:
        prec2 = int(1.2 * (prec + 10))
        asign, aman, aexp, abc = a
        bsign, bman, bexp, bbc = b
        pf = mpc_abs((a,b), prec)
        if pf[-2] + pf[-1] > -10  and pf[-2] + pf[-1] < prec:
            af = to_fixed(a, prec2)
            bf = to_fixed(b, prec2)
            re, im = mpc_nthroot_fixed(af, bf, n, prec2)
            extra = 10
            re = from_man_exp(re, -prec2-extra, prec2, rnd)
            im = from_man_exp(im, -prec2-extra, prec2, rnd)
            return re, im
    fn = from_int(n)
    prec2 = prec+10 + 10
    nth = mpf_rdiv_int(1, fn, prec2)
    re, im = mpc_pow((a, b), (nth, fzero), prec2, rnd)
    re = normalize(re[0], re[1], re[2], re[3], prec, rnd)
    im = normalize(im[0], im[1], im[2], im[3], prec, rnd)
    return re, im

