
def test_Multinomial():
    n, x1, x2, x3, x4 = symbols('n, x1, x2, x3, x4', nonnegative=True, integer=True)
    p1, p2, p3, p4 = symbols('p1, p2, p3, p4', positive=True)
    p1_f, n_f = symbols('p1_f, n_f', negative=True)
    M = Multinomial('M', n, [p1, p2, p3, p4])
    C = Multinomial('C', 3, p1, p2, p3)
    f = factorial
    assert density(M)(x1, x2, x3, x4) == Piecewise((p1**x1*p2**x2*p3**x3*p4**x4*
                                            f(n)/(f(x1)*f(x2)*f(x3)*f(x4)),
                                            Eq(n, x1 + x2 + x3 + x4)), (0, True))
    assert marginal_distribution(C, C[0])(x1).subs(x1, 1) ==\
                                                            3*p1*p2**2 +\
                                                            6*p1*p2*p3 +\
                                                            3*p1*p3**2
    raises(ValueError, lambda: Multinomial('b1', 5, [p1, p2, p3, p1_f]))
    raises(ValueError, lambda: Multinomial('b2', n_f, [p1, p2, p3, p4]))
    raises(ValueError, lambda: Multinomial('b3', n, 0.5, 0.4, 0.3, 0.1))

