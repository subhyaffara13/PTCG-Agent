
def test_issue_8601():
    n = Symbol('n', integer=True, negative=True)

    assert catalan(n - 1) is S.Zero
    assert catalan(Rational(-1, 2)) is S.ComplexInfinity
    assert catalan(-S.One) == Rational(-1, 2)
    c1 = catalan(-5.6).evalf()
    assert str(c1) == '6.93334070531408e-5'
    c2 = catalan(-35.4).evalf()
    assert str(c2) == '-4.14189164517449e-24'

