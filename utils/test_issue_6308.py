
def test_issue_6308():
    k, a0 = symbols('k a0', real=True)
    assert integrate((x**2 + 1 - k**2)/(x**2 + 1 + a0**2), x) == \
        x - (a0**2 + k**2)*atan(x/sqrt(a0**2 + 1))/sqrt(a0**2 + 1)

