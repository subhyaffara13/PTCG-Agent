
def _transformation_e(f, x, P, Q, k, m):
    f = f.diff(x)
    P = P.subs(k, k + 1) * (k + m + 1)
    Q = Q.subs(k, k + 1) * (k + 1)
    return f, P, Q, m

