
def test_issue_3796():
    assert manualintegrate(diff(exp(x + x**2)), x) == exp(x + x**2)
    assert integrate(x * exp(x**4), x, risch=False) == -I*sqrt(pi)*erf(I*x**2)/4

