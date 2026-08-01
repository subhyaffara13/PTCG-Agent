
def test_double_previously_failing_integrals():
    # Double integrals not implemented <- Sure it is!
    res = integrate(sqrt(x) + x*y, (x, 1, 2), (y, -1, 1))
    # Old numerical test
    assert NS(res, 15) == '2.43790283299492'
    # Symbolic test
    assert res == Rational(-4, 3) + 8*sqrt(2)/3
    # double integral + zero detection
    assert integrate(sin(x + x*y), (x, -1, 1), (y, -1, 1)) is S.Zero

