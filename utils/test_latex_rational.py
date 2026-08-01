
def test_latex_rational():
    # tests issue 3973
    assert latex(-Rational(1, 2)) == r"- \frac{1}{2}"
    assert latex(Rational(-1, 2)) == r"- \frac{1}{2}"
    assert latex(Rational(1, -2)) == r"- \frac{1}{2}"
    assert latex(-Rational(-1, 2)) == r"\frac{1}{2}"
    assert latex(-Rational(1, 2)*x) == r"- \frac{x}{2}"
    assert latex(-Rational(1, 2)*x + Rational(-2, 3)*y) == \
        r"- \frac{x}{2} - \frac{2 y}{3}"

