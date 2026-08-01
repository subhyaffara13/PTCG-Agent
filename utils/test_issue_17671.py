
def test_issue_17671():
    assert limit(Ei(-log(x)) - log(log(x))/x, x, 1) == EulerGamma


def test_issue_17671():
    assert integrate(log(log(x)) / x**2, [x, 1, oo]) == -EulerGamma
    assert integrate(log(log(x)) / x**3, [x, 1, oo]) == -log(2)/2 - EulerGamma/2
    assert integrate(log(log(x)) / x**10, [x, 1, oo]) == -log(9)/9 - EulerGamma/9

