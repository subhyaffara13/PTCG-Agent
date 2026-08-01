
def test_issue_8368():
    assert meijerint_indefinite(cosh(x)*exp(-x*t), x) == (
        (-t - 1)*exp(x) + (-t + 1)*exp(-x))*exp(-t*x)/2/(t**2 - 1)

