
def test_MultivariateEwens():
    n, theta, i = symbols('n theta i', positive=True)

    # tests for integer dimensions
    theta_f = symbols('t_f', negative=True)
    a = symbols('a_1:4', positive = True, integer = True)
    ed = MultivariateEwens('E', 3, theta)
    assert density(ed)(a[0], a[1], a[2]) == Piecewise((6*2**(-a[1])*3**(-a[2])*
                                            theta**a[0]*theta**a[1]*theta**a[2]/
                                            (theta*(theta + 1)*(theta + 2)*
                                            factorial(a[0])*factorial(a[1])*
                                            factorial(a[2])), Eq(a[0] + 2*a[1] +
                                            3*a[2], 3)), (0, True))
    assert marginal_distribution(ed, ed[1])(a[1]) == Piecewise((6*2**(-a[1])*
                                                    theta**a[1]/((theta + 1)*
                                                    (theta + 2)*factorial(a[1])),
                                                    Eq(2*a[1] + 1, 3)), (0, True))
    raises(ValueError, lambda: MultivariateEwens('e1', 5, theta_f))
    assert ed.pspace.distribution.set == ProductSet(Range(0, 4, 1),
                                            Range(0, 2, 1), Range(0, 2, 1))

    # tests for symbolic dimensions
    eds = MultivariateEwens('E', n, theta)
    a = IndexedBase('a')
    j, k = symbols('j, k')
    den = Piecewise((factorial(n)*Product(theta**a[j]*(j + 1)**(-a[j])/
           factorial(a[j]), (j, 0, n - 1))/RisingFactorial(theta, n),
            Eq(n, Sum((k + 1)*a[k], (k, 0, n - 1)))), (0, True))
    assert density(eds)(a).dummy_eq(den)

