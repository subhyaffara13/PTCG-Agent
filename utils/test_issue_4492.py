
def test_issue_4492():
    assert simplify(integrate(x**2 * sqrt(5 - x**2), x)).factor(
        deep=True) == Piecewise(
        (I*(2*x**5 - 15*x**3 + 25*x - 25*sqrt(x**2 - 5)*acosh(sqrt(5)*x/5)) /
            (8*sqrt(x**2 - 5)), (x > sqrt(5)) | (x < -sqrt(5))),
        ((2*x**5 - 15*x**3 + 25*x - 25*sqrt(5 - x**2)*asin(sqrt(5)*x/5)) /
            (-8*sqrt(-x**2 + 5)), True))

