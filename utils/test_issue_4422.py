
def test_issue_4422():
    assert integrate(1/sqrt(16 + 4*x**2), x) == asinh(x/2) / 2

