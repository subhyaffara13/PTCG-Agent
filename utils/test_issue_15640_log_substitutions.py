
def test_issue_15640_log_substitutions():
    f = x/log(x)
    F = Ei(2*log(x))
    assert integrate(f, x) == F and F.diff(x) == f
    f = x**3/log(x)**2
    F = -x**4/log(x) + 4*Ei(4*log(x))
    assert integrate(f, x) == F and F.diff(x) == f
    f = sqrt(log(x))/x**2
    F = -sqrt(pi)*erfc(sqrt(log(x)))/2 - sqrt(log(x))/x
    assert integrate(f, x) == F and F.diff(x) == f

