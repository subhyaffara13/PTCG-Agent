
def _transformation_a(f, x, P, Q, k, m, shift):
    f *= x**(-shift)
    P = P.subs(k, k + shift)
    Q = Q.subs(k, k + shift)
    return f, P, Q, m

