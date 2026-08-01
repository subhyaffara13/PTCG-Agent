
def mpc_div(z, w, prec, rnd=round_fast):
    a, b = z
    c, d = w
    wp = prec + 10
    # mag = c*c + d*d
    mag = mpf_add(mpf_mul(c, c), mpf_mul(d, d), wp)
    # (a*c+b*d)/mag, (b*c-a*d)/mag
    t = mpf_add(mpf_mul(a,c), mpf_mul(b,d), wp)
    u = mpf_sub(mpf_mul(b,c), mpf_mul(a,d), wp)
    return mpf_div(t,mag,prec,rnd), mpf_div(u,mag,prec,rnd)

