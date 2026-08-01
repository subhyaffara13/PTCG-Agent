
def test_issue_8882():
    # This is the original test.
    # from sympy import diff, Integral, integrate
    # r = Symbol('r')
    # psi = 1/r*sin(r)*exp(-(a0*r))
    # h = -1/2*diff(psi, r, r) - 1/r*psi
    # f = 4*pi*psi*h*r**2
    # assert integrate(f, (r, -oo, 3), meijerg=True).has(Integral) == True

    # To save time, only the critical part is included.
    F = -a**(-s + 1)*(4 + 1/a**2)**(-s/2)*sqrt(1/a**2)*exp(-s*I*pi)* \
        sin(s*atan(sqrt(1/a**2)/2))*gamma(s)
    raises(IntegralTransformError, lambda:
        inverse_mellin_transform(F, s, x, (-1, oo),
        **{'as_meijerg': True, 'needeval': True}))

