
def cos_sin_quadrant(x, wp):
    sign, man, exp, bc = x
    if x == fzero:
        return fone, fzero, 0
    # TODO: combine evaluation code to avoid duplicate modulo
    c, s = mpf_cos_sin(x, wp)
    t, n, wp_ = mod_pi2(man, exp, exp+bc, 15)
    if sign:
        n = -1-n
    return c, s, n

