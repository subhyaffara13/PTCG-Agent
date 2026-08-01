
def mpc_fibonacci(z, prec, rnd=round_fast):
    re, im = z
    if im == fzero:
        return (mpf_fibonacci(re, prec, rnd), fzero)
    size = max(abs(re[2]+re[3]), abs(re[2]+re[3]))
    wp = prec + size + 20
    a = mpf_phi(wp)
    b = mpf_add(mpf_shift(a, 1), fnone, wp)
    u = mpc_pow((a, fzero), z, wp)
    v = mpc_cos_pi(z, wp)
    v = mpc_div(v, u, wp)
    u = mpc_sub(u, v, wp)
    u = mpc_div_mpf(u, b, prec, rnd)
    return u

