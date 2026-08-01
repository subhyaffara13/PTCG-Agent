
def test_issue_8520():
    assert manualintegrate(x/(x**4 + 1), x) == atan(x**2)/2
    assert manualintegrate(x**2/(x**6 + 25), x) == atan(x**3/5)/15
    f = x/(9*x**4 + 4)**2
    assert manualintegrate(f, x).diff(x).factor() == f

