
def test_issue_7337():
    f = meijerint_indefinite(x*sqrt(2*x + 3), x).together()
    assert f == sqrt(2*x + 3)*(2*x**2 + x - 3)/5
    assert f._eval_interval(x, S.NegativeOne, S.One) == Rational(2, 5)

