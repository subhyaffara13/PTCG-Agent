
def test_issue_22453():
    from sympy.utilities.iterables import cartes
    e = Symbol('e', extended_positive=True)
    for a, b in cartes(*[[oo, -oo, 3]]*2):
        if a == b == 3:
            continue
        i = a + I*b
        assert i**(1 + e) is S.ComplexInfinity
        assert i**-e is S.Zero
        assert unchanged(Pow, i, e)
    assert 1/(oo + I*oo) is S.Zero
    r, i = [Dummy(infinite=True, extended_real=True) for _ in range(2)]
    assert 1/(r + I*i) is S.Zero
    assert 1/(3 + I*i) is S.Zero
    assert 1/(r + I*3) is S.Zero

