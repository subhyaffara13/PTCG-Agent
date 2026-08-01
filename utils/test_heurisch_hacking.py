
def test_heurisch_hacking():
    assert heurisch(sqrt(1 + 7*x**2), x, hints=[]) == \
        x*sqrt(1 + 7*x**2)/2 + sqrt(7)*asinh(sqrt(7)*x)/14
    assert heurisch(sqrt(1 - 7*x**2), x, hints=[]) == \
        x*sqrt(1 - 7*x**2)/2 + sqrt(7)*asin(sqrt(7)*x)/14

    assert heurisch(1/sqrt(1 + 7*x**2), x, hints=[]) == \
        sqrt(7)*asinh(sqrt(7)*x)/7
    assert heurisch(1/sqrt(1 - 7*x**2), x, hints=[]) == \
        sqrt(7)*asin(sqrt(7)*x)/7

    assert heurisch(exp(-7*x**2), x, hints=[]) == \
        sqrt(7*pi)*erf(sqrt(7)*x)/14

    assert heurisch(1/sqrt(9 - 4*x**2), x, hints=[]) == \
        asin(x*Rational(2, 3))/2

    assert heurisch(1/sqrt(9 + 4*x**2), x, hints=[]) == \
        asinh(x*Rational(2, 3))/2

    assert heurisch(1/sqrt(3*x**2-4), x, hints=[]) == \
           sqrt(3)*log(3*x + sqrt(3)*sqrt(3*x**2 - 4))/3

