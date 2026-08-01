
def test_PoissonProcess():
    X = PoissonProcess("X", 3)
    assert X.state_space == S.Naturals0
    assert X.index_set == Interval(0, oo)
    assert X.lamda == 3

    t, d, x, y = symbols('t d x y', positive=True)
    assert isinstance(X(t), RandomIndexedSymbol)
    assert X.distribution(t) == PoissonDistribution(3*t)
    with warns_deprecated_sympy():
        X.distribution(X(t))
    raises(ValueError, lambda: PoissonProcess("X", -1))
    raises(NotImplementedError, lambda: X[t])
    raises(IndexError, lambda: X(-5))

    assert X.joint_distribution(X(2), X(3)) == JointDistributionHandmade(Lambda((X(2), X(3)),
                6**X(2)*9**X(3)*exp(-15)/(factorial(X(2))*factorial(X(3)))))

    assert X.joint_distribution(4, 6) == JointDistributionHandmade(Lambda((X(4), X(6)),
                12**X(4)*18**X(6)*exp(-30)/(factorial(X(4))*factorial(X(6)))))

    assert P(X(t) < 1) == exp(-3*t)
    assert P(Eq(X(t), 0), Contains(t, Interval.Lopen(3, 5))) == exp(-6) # exp(-2*lamda)
    res = P(Eq(X(t), 1), Contains(t, Interval.Lopen(3, 4)))
    assert res == 3*exp(-3)

    # Equivalent to P(Eq(X(t), 1))**4 because of non-overlapping intervals
    assert P(Eq(X(t), 1) & Eq(X(d), 1) & Eq(X(x), 1) & Eq(X(y), 1), Contains(t, Interval.Lopen(0, 1))
    & Contains(d, Interval.Lopen(1, 2)) & Contains(x, Interval.Lopen(2, 3))
    & Contains(y, Interval.Lopen(3, 4))) == res**4

    # Return Probability because of overlapping intervals
    assert P(Eq(X(t), 2) & Eq(X(d), 3), Contains(t, Interval.Lopen(0, 2))
    & Contains(d, Interval.Ropen(2, 4))) == \
                Probability(Eq(X(d), 3) & Eq(X(t), 2), Contains(t, Interval.Lopen(0, 2))
                & Contains(d, Interval.Ropen(2, 4)))

    raises(ValueError, lambda: P(Eq(X(t), 2) & Eq(X(d), 3),
    Contains(t, Interval.Lopen(0, 4)) & Contains(d, Interval.Lopen(3, oo)))) # no bound on d
    assert P(Eq(X(3), 2)) == 81*exp(-9)/2
    assert P(Eq(X(t), 2), Contains(t, Interval.Lopen(0, 5))) == 225*exp(-15)/2

    # Check that probability works correctly by adding it to 1
    res1 = P(X(t) <= 3, Contains(t, Interval.Lopen(0, 5)))
    res2 = P(X(t) > 3, Contains(t, Interval.Lopen(0, 5)))
    assert res1 == 691*exp(-15)
    assert (res1 + res2).simplify() == 1

    # Check Not and  Or
    assert P(Not(Eq(X(t), 2) & (X(d) > 3)), Contains(t, Interval.Ropen(2, 4)) & \
            Contains(d, Interval.Lopen(7, 8))).simplify() == -18*exp(-6) + 234*exp(-9) + 1
    assert P(Eq(X(t), 2) | Ne(X(t), 4), Contains(t, Interval.Ropen(2, 4))) == 1 - 36*exp(-6)
    raises(ValueError, lambda: P(X(t) > 2, X(t) + X(d)))
    assert E(X(t)) == 3*t  # property of the distribution at a given timestamp
    assert E(X(t)**2 + X(d)*2 + X(y)**3, Contains(t, Interval.Lopen(0, 1))
        & Contains(d, Interval.Lopen(1, 2)) & Contains(y, Interval.Ropen(3, 4))) == 75
    assert E(X(t)**2, Contains(t, Interval.Lopen(0, 1))) == 12
    assert E(x*(X(t) + X(d))*(X(t)**2+X(d)**2), Contains(t, Interval.Lopen(0, 1))
    & Contains(d, Interval.Ropen(1, 2))) == \
            Expectation(x*(X(d) + X(t))*(X(d)**2 + X(t)**2), Contains(t, Interval.Lopen(0, 1))
            & Contains(d, Interval.Ropen(1, 2)))

    # Value Error because of infinite time bound
    raises(ValueError, lambda: E(X(t)**3, Contains(t, Interval.Lopen(1, oo))))

    # Equivalent to E(X(t)**2) - E(X(d)**2) == E(X(1)**2) - E(X(1)**2) == 0
    assert E((X(t) + X(d))*(X(t) - X(d)), Contains(t, Interval.Lopen(0, 1))
        & Contains(d, Interval.Lopen(1, 2))) == 0
    assert E(X(2) + x*E(X(5))) == 15*x + 6
    assert E(x*X(1) + y) == 3*x + y
    assert P(Eq(X(1), 2) & Eq(X(t), 3), Contains(t, Interval.Lopen(1, 2))) == 81*exp(-6)/4
    Y = PoissonProcess("Y", 6)
    Z = X + Y
    assert Z.lamda == X.lamda + Y.lamda == 9
    raises(ValueError, lambda: X + 5) # should be added be only PoissonProcess instance
    N, M = Z.split(4, 5)
    assert N.lamda == 4
    assert M.lamda == 5
    raises(ValueError, lambda: Z.split(3, 2)) # 2+3 != 9

    raises(ValueError, lambda :P(Eq(X(t), 0), Contains(t, Interval.Lopen(1, 3)) & Eq(X(1), 0)))
    # check if it handles queries with two random variables in one args
    res1 = P(Eq(N(3), N(5)))
    assert res1 == P(Eq(N(t), 0), Contains(t, Interval(3, 5)))
    res2 = P(N(3) > N(1))
    assert res2 == P((N(t) > 0), Contains(t, Interval(1, 3)))
    assert P(N(3) < N(1)) == 0 # condition is not possible
    res3 = P(N(3) <= N(1)) # holds only for Eq(N(3), N(1))
    assert res3 == P(Eq(N(t), 0), Contains(t, Interval(1, 3)))

    # tests from https://www.probabilitycourse.com/chapter11/11_1_2_basic_concepts_of_the_poisson_process.php
    X = PoissonProcess('X', 10) # 11.1
    assert P(Eq(X(S(1)/3), 3) & Eq(X(1), 10)) == exp(-10)*Rational(8000000000, 11160261)
    assert P(Eq(X(1), 1), Eq(X(S(1)/3), 3)) == 0
    assert P(Eq(X(1), 10), Eq(X(S(1)/3), 3)) == P(Eq(X(S(2)/3), 7))

    X = PoissonProcess('X', 2) # 11.2
    assert P(X(S(1)/2) < 1) == exp(-1)
    assert P(X(3) < 1, Eq(X(1), 0)) == exp(-4)
    assert P(Eq(X(4), 3), Eq(X(2), 3)) == exp(-4)

    X = PoissonProcess('X', 3)
    assert P(Eq(X(2), 5) & Eq(X(1), 2)) == Rational(81, 4)*exp(-6)

    # check few properties
    assert P(X(2) <= 3, X(1)>=1) == 3*P(Eq(X(1), 0)) + 2*P(Eq(X(1), 1)) + P(Eq(X(1), 2))
    assert P(X(2) <= 3, X(1) > 1) == 2*P(Eq(X(1), 0)) + 1*P(Eq(X(1), 1))
    assert P(Eq(X(2), 5) & Eq(X(1), 2)) == P(Eq(X(1), 3))*P(Eq(X(1), 2))
    assert P(Eq(X(3), 4), Eq(X(1), 3)) == P(Eq(X(2), 1))

    #test issue 20078
    assert (2*X(t) + 3*X(t)).simplify() == 5*X(t)
    assert (2*X(t) - 3*X(t)).simplify() == -X(t)
    assert (2*(0.25*X(t))).simplify() == 0.5*X(t)
    assert (2*X(t) * 0.25*X(t)).simplify() == 0.5*X(t)**2
    assert (X(t)**2 + X(t)**3).simplify() == (X(t) + 1)*X(t)**2

