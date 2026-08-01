
def test_GammaProcess_numeric():
    t, d, x, y = symbols('t d x y', positive=True)
    X = GammaProcess("X", 1, 2)
    assert X.state_space == Interval(0, oo)
    assert X.index_set == Interval(0, oo)
    assert X.lamda == 1
    assert X.gamma == 2

    raises(ValueError, lambda: GammaProcess("X", -1, 2))
    raises(ValueError, lambda: GammaProcess("X", 0, -2))
    raises(ValueError, lambda: GammaProcess("X", -1, -2))

    # all are independent because of non-overlapping intervals
    assert P((X(t) > 4) & (X(d) > 3) & (X(x) > 2) & (X(y) > 1), Contains(t,
        Interval.Lopen(0, 1)) & Contains(d, Interval.Lopen(1, 2)) & Contains(x,
        Interval.Lopen(2, 3)) & Contains(y, Interval.Lopen(3, 4))).simplify() == \
                                                            120*exp(-10)

    # Check working with Not and Or
    assert P(Not((X(t) < 5) & (X(d) > 3)), Contains(t, Interval.Ropen(2, 4)) &
        Contains(d, Interval.Lopen(7, 8))).simplify() == -4*exp(-3) + 472*exp(-8)/3 + 1
    assert P((X(t) > 2) | (X(t) < 4), Contains(t, Interval.Ropen(1, 4))).simplify() == \
                                            -643*exp(-4)/15 + 109*exp(-2)/15 + 1

    assert E(X(t)) == 2*t # E(X(t)) == gamma*t/l
    assert E(X(2) + x*E(X(5))) == 10*x + 4

