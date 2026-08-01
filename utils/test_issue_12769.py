
def test_issue_12769():
    r, z, x = symbols('r z x', real=True)
    a, b, s0, K, F0, s, T = symbols('a b s0 K F0 s T', positive=True, real=True)
    fx = (F0**b*K**b*r*s0 - sqrt((F0**2*K**(2*b)*a**2*(b - 1) + \
        F0**(2*b)*K**2*a**2*(b - 1) + F0**(2*b)*K**(2*b)*s0**2*(b - 1)*(b**2 - 2*b + 1) - \
        2*F0**(2*b)*K**(b + 1)*a*r*s0*(b**2 - 2*b +  1) + \
        2*F0**(b + 1)*K**(2*b)*a*r*s0*(b**2 - 2*b + 1) - \
        2*F0**(b + 1)*K**(b + 1)*a**2*(b - 1))/((b - 1)*(b**2 - 2*b + 1))))*(b*r -  b - r + 1)

    assert fx.subs(K, F0).factor(deep=True) == limit(fx, K, F0).factor(deep=True)

