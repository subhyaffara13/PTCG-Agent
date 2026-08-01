
def test_errorinverses():
    assert solve(erf(x) - y, x) == [erfinv(y)]
    assert solve(erfinv(x) - y, x) == [erf(y)]
    assert solve(erfc(x) - y, x) == [erfcinv(y)]
    assert solve(erfcinv(x) - y, x) == [erfc(y)]


def test_errorinverses():
    assert solveset_real(erf(x) - S.Half, x) == \
        FiniteSet(erfinv(S.Half))
    assert solveset_real(erfinv(x) - 2, x) == \
        FiniteSet(erf(2))
    assert solveset_real(erfc(x) - S.One, x) == \
        FiniteSet(erfcinv(S.One))
    assert solveset_real(erfcinv(x) - 2, x) == FiniteSet(erfc(2))

