
def test_gamma_as_leading_term():
    assert gamma(x).as_leading_term(x) == 1/x
    assert gamma(2 + x).as_leading_term(x) == S(1)
    assert gamma(cos(x)).as_leading_term(x) == S(1)
    assert gamma(sin(x)).as_leading_term(x) == 1/x

