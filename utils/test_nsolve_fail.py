
def test_nsolve_fail():
    x = symbols('x')
    # Sometimes it is better to use the numerator (issue 4829)
    # but sometimes it is not (issue 11768) so leave this to
    # the discretion of the user
    ans = nsolve(x**2/(1 - x)/(1 - 2*x)**2 - 100, x, 0)
    assert ans > 0.46 and ans < 0.47

