
def mertens_fixed(prec):
    wp = prec + 20
    m = 2
    s = mpf_euler(wp)
    while 1:
        t = mpf_zeta_int(m, wp)
        if t == fone:
            break
        t = mpf_log(t, wp)
        t = mpf_mul_int(t, moebius(m), wp)
        t = mpf_div(t, from_int(m), wp)
        s = mpf_add(s, t)
        m += 1
    return to_fixed(s, prec)

