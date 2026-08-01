
def test_issue_9858():
    assert manualintegrate(exp(x)*cos(exp(x)), x) == sin(exp(x))
    assert manualintegrate(exp(2*x)*cos(exp(x)), x) == \
        exp(x)*sin(exp(x)) + cos(exp(x))
    res = manualintegrate(exp(10*x)*sin(exp(x)), x)
    assert not res.has(Integral)
    assert res.diff(x) == exp(10*x)*sin(exp(x))
    # an example with many similar integrations by parts
    assert manualintegrate(sum(x*exp(k*x) for k in range(1, 8)), x) == (
        x*exp(7*x)/7 + x*exp(6*x)/6 + x*exp(5*x)/5 + x*exp(4*x)/4 +
        x*exp(3*x)/3 + x*exp(2*x)/2 + x*exp(x) - exp(7*x)/49 -exp(6*x)/36 -
        exp(5*x)/25 - exp(4*x)/16 - exp(3*x)/9 - exp(2*x)/4 - exp(x))

