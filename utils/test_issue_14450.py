
def test_issue_14450():
    assert uppergamma(Rational(3, 8), x).evalf() == uppergamma(Rational(3, 8), x)
    assert lowergamma(x, Rational(3, 8)).evalf() == lowergamma(x, Rational(3, 8))
    # some values from Wolfram Alpha for comparison
    assert abs(uppergamma(Rational(3, 8), 2).evalf() - 0.07105675881) < 1e-9
    assert abs(lowergamma(Rational(3, 8), 2).evalf() - 2.2993794256) < 1e-9

