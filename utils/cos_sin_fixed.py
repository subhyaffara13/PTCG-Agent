
def cos_sin_fixed(x, prec, pi2=None):
    if pi2 is None:
        pi2 = pi_fixed(prec-1)
    n, t = divmod(x, pi2)
    n = int(n)
    c, s = cos_sin_basecase(t, prec)
    m = n & 3
    if m == 0: return c, s
    if m == 1: return -s, c
    if m == 2: return -c, -s
    if m == 3: return s, -c

