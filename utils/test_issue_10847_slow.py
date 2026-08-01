
def test_issue_10847_slow():
    assert manualintegrate((4*x**4 + 4*x**3 + 16*x**2 + 12*x + 8)
                           / (x**6 + 2*x**5 + 3*x**4 + 4*x**3 + 3*x**2 + 2*x + 1), x) == \
                           2*x/(x**2 + 1) + 3*atan(x) - 1/(x**2 + 1) - 3/(x + 1)

