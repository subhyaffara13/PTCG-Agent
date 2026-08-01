
def test_bessely_leading_term():
    assert bessely(0, x).as_leading_term(x) == (2*log(x) - 2*log(2) + 2*S.EulerGamma)/pi
    assert bessely(1, sin(x)).as_leading_term(x) == -2/(pi*x)
    assert bessely(1, 2*sqrt(x)).as_leading_term(x) == -1/(pi*sqrt(x))

