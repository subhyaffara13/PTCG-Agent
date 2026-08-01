
def test_GammaProcess_symbolic():
    t, d, x, y, g, l = symbols('t d x y g l', positive=True)
    X = GammaProcess("X", l, g)

    raises(NotImplementedError, lambda: X[t])
    raises(IndexError, lambda: X(-1))
    assert isinstance(X(t), RandomIndexedSymbol)
    assert X.state_space == Interval(0, oo)
    assert X.distribution(t) == GammaDistribution(g*t, 1/l)
    with warns_deprecated_sympy():
        X.distribution(X(t))
    assert X.joint_distribution(5, X(3)) == JointDistributionHandmade(Lambda(
        (X(5), X(3)), l**(8*g)*exp(-l*X(3))*exp(-l*X(5))*X(3)**(3*g - 1)*X(5)**(5*g
        - 1)/(gamma(3*g)*gamma(5*g))))
    # property of the gamma process at any given timestamp
    assert E(X(t)) == g*t/l
    assert variance(X(t)).simplify() == g*t/l**2

    # Equivalent to E(2*X(1)) + E(X(1)**2) + E(X(1)**3), where E(X(1)) == g/l
    assert E(X(t)**2 + X(d)*2 + X(y)**3, Contains(t, Interval.Lopen(0, 1))
        & Contains(d, Interval.Lopen(1, 2)) & Contains(y, Interval.Ropen(3, 4))) == \
            2*g/l + (g**2 + g)/l**2 + (g**3 + 3*g**2 + 2*g)/l**3

    assert P(X(t) > 3, Contains(t, Interval.Lopen(3, 4))).simplify() == \
                                1 - lowergamma(g, 3*l)/gamma(g) # equivalent to P(X(1)>3)


    #test issue 20078
    assert (2*X(t) + 3*X(t)).simplify() == 5*X(t)
    assert (2*X(t) - 3*X(t)).simplify() == -X(t)
    assert (2*(0.25*X(t))).simplify() == 0.5*X(t)
    assert (2*X(t) * 0.25*X(t)).simplify() == 0.5*X(t)**2
    assert (X(t)**2 + X(t)**3).simplify() == (X(t) + 1)*X(t)**2

