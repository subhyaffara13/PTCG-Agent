
def test_issue_8245():
    a = S("6506833320952669167898688709329/5070602400912917605986812821504")
    assert rel_check(a, a.n(10))
    assert rel_check(a, a.n(20))
    assert rel_check(a, a.n())
    # prec of 31 is enough to fully capture a as mpf
    assert Float(a, 31) == Float(str(a.p), '')/Float(str(a.q), '')
    for i in range(31):
        r = Rational(Float(a, i))
        f = Float(r)
        assert (f < a) == (Rational(f) < a)
    # test sign handling
    assert (-f < -a) == (Rational(-f) < -a)
    # test equivalence handling
    isa = Float(a.p,'')/Float(a.q,'')
    assert isa <= a
    assert not isa < a
    assert isa >= a
    assert not isa > a
    assert isa > 0

    a = sqrt(2)
    r = Rational(str(a.n(30)))
    assert rel_check(a, r)

    a = sqrt(2)
    r = Rational(str(a.n(29)))
    assert rel_check(a, r)

    assert Eq(log(cos(2)**2 + sin(2)**2), 0) is S.true

