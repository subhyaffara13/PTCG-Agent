
def test_issue_3952():
    f = sin(x)
    assert integrate(f, x) == -cos(x)
    raises(ValueError, lambda: integrate(f, 2*x))

