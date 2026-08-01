
def construct_d_case_6(num, den, x):
    # s_oo = lim x->0 1/x**2 * a(1/x) which is equivalent to
    # s_oo = lim x->oo x**2 * a(x)
    s_inf = limit_at_inf(Poly(x**2, x)*num, den, x)

    # d_(-1) = (1 +- sqrt(1 + 4*s_oo))/2
    if s_inf != -S(1)/4:
        return [[(1 + sqrt(1 + 4*s_inf))/2], [(1 - sqrt(1 + 4*s_inf))/2]]
    return [[S.Half]]

