
def test_issues_13081_12583_12534():
    # 13081
    r = Rational('905502432259640373/288230376151711744')
    assert (r < pi) is S.false
    assert (r > pi) is S.true
    # 12583
    v = sqrt(2)
    u = sqrt(v) + 2/sqrt(10 - 8/sqrt(2 - v) + 4*v*(1/sqrt(2 - v) - 1))
    assert (u >= 0) is S.true
    # 12534; Rational vs NumberSymbol
    # here are some precisions for which Rational forms
    # at a lower and higher precision bracket the value of pi
    # e.g. for p = 20:
    # Rational(pi.n(p + 1)).n(25) = 3.14159265358979323846 2834
    #                    pi.n(25) = 3.14159265358979323846 2643
    # Rational(pi.n(p    )).n(25) = 3.14159265358979323846 1987
    assert [p for p in range(20, 50) if
            (Rational(pi.n(p)) < pi) and
            (pi < Rational(pi.n(p + 1)))] == [20, 24, 27, 33, 37, 43, 48]
    # pick one such precision and affirm that the reversed operation
    # gives the opposite result, i.e. if x < y is true then x > y
    # must be false
    for i in (20, 21):
        v = pi.n(i)
        assert rel_check(Rational(v), pi)
        assert rel_check(v, pi)
    assert rel_check(pi.n(20), pi.n(21))
    # Float vs Rational
    # the rational form is less than the floating representation
    # at the same precision
    assert [i for i in range(15, 50) if Rational(pi.n(i)) > pi.n(i)] == []
    # this should be the same if we reverse the relational
    assert [i for i in range(15, 50) if pi.n(i) < Rational(pi.n(i))] == []

