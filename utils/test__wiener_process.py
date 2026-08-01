
def test_WienerProcess():
    X = WienerProcess("X")
    assert X.state_space == S.Reals
    assert X.index_set == Interval(0, oo)

    t, d, x, y = symbols('t d x y', positive=True)
    assert isinstance(X(t), RandomIndexedSymbol)
    assert X.distribution(t) == NormalDistribution(0, sqrt(t))
    with warns_deprecated_sympy():
        X.distribution(X(t))
    raises(ValueError, lambda: PoissonProcess("X", -1))
    raises(NotImplementedError, lambda: X[t])
    raises(IndexError, lambda: X(-2))

    assert X.joint_distribution(X(2), X(3)) == JointDistributionHandmade(
        Lambda((X(2), X(3)), sqrt(6)*exp(-X(2)**2/4)*exp(-X(3)**2/6)/(12*pi)))
    assert X.joint_distribution(4, 6) == JointDistributionHandmade(
        Lambda((X(4), X(6)), sqrt(6)*exp(-X(4)**2/8)*exp(-X(6)**2/12)/(24*pi)))

    assert P(X(t) < 3).simplify() == erf(3*sqrt(2)/(2*sqrt(t)))/2 + S(1)/2
    assert P(X(t) > 2, Contains(t, Interval.Lopen(3, 7))).simplify() == S(1)/2 -\
                erf(sqrt(2)/2)/2

    # Equivalent to P(X(1)>1)**4
    assert P((X(t) > 4) & (X(d) > 3) & (X(x) > 2) & (X(y) > 1),
        Contains(t, Interval.Lopen(0, 1)) & Contains(d, Interval.Lopen(1, 2))
        & Contains(x, Interval.Lopen(2, 3)) & Contains(y, Interval.Lopen(3, 4))).simplify() ==\
        (1 - erf(sqrt(2)/2))*(1 - erf(sqrt(2)))*(1 - erf(3*sqrt(2)/2))*(1 - erf(2*sqrt(2)))/16

    # Contains an overlapping interval so, return Probability
    assert P((X(t)< 2) & (X(d)> 3), Contains(t, Interval.Lopen(0, 2))
        & Contains(d, Interval.Ropen(2, 4))) == Probability((X(d) > 3) & (X(t) < 2),
        Contains(d, Interval.Ropen(2, 4)) & Contains(t, Interval.Lopen(0, 2)))

    assert str(P(Not((X(t) < 5) & (X(d) > 3)), Contains(t, Interval.Ropen(2, 4)) &
        Contains(d, Interval.Lopen(7, 8))).simplify()) == \
                '-(1 - erf(3*sqrt(2)/2))*(2 - erfc(5/2))/4 + 1'
    # Distribution has mean 0 at each timestamp
    assert E(X(t)) == 0
    assert E(x*(X(t) + X(d))*(X(t)**2+X(d)**2), Contains(t, Interval.Lopen(0, 1))
    & Contains(d, Interval.Ropen(1, 2))) == Expectation(x*(X(d) + X(t))*(X(d)**2 + X(t)**2),
    Contains(d, Interval.Ropen(1, 2)) & Contains(t, Interval.Lopen(0, 1)))
    assert E(X(t) + x*E(X(3))) == 0

    #test issue 20078
    assert (2*X(t) + 3*X(t)).simplify() == 5*X(t)
    assert (2*X(t) - 3*X(t)).simplify() == -X(t)
    assert (2*(0.25*X(t))).simplify() == 0.5*X(t)
    assert (2*X(t) * 0.25*X(t)).simplify() == 0.5*X(t)**2
    assert (X(t)**2 + X(t)**3).simplify() == (X(t) + 1)*X(t)**2

