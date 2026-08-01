
def test_M23():
    x = symbols('x', complex=True)
    # TODO: Replace solve with solveset, as of now test fails for solveset
    assert solve(x - 1/sqrt(1 + x**2)) == [
        -I*sqrt(S.Half + sqrt(5)/2), sqrt(Rational(-1, 2) + sqrt(5)/2)]

