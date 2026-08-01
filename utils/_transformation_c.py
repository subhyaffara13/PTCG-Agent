
def _transformation_c(f, x, P, Q, k, m, scale):
    f = f.subs(x, x**scale)
    P = P.subs(k, k / scale)
    Q = Q.subs(k, k / scale)
    m *= scale
    return f, P, Q, m

