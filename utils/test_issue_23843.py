
def test_issue_23843():
    #atan
    assert atan(x + I).series(x, oo) == -16/(5*x**5) - 2*I/x**4 + 4/(3*x**3) + I/x**2 - 1/x + pi/2 + O(x**(-6), (x, oo))
    assert atan(x + I).series(x, -oo) == -16/(5*x**5) - 2*I/x**4 + 4/(3*x**3) + I/x**2 - 1/x - pi/2 + O(x**(-6), (x, -oo))
    assert atan(x - I).series(x, oo) == -16/(5*x**5) + 2*I/x**4 + 4/(3*x**3) - I/x**2 - 1/x + pi/2 + O(x**(-6), (x, oo))
    assert atan(x - I).series(x, -oo) == -16/(5*x**5) + 2*I/x**4 + 4/(3*x**3) - I/x**2 - 1/x - pi/2 + O(x**(-6), (x, -oo))

    #acot
    assert acot(x + I).series(x, oo) == 16/(5*x**5) + 2*I/x**4 - 4/(3*x**3) - I/x**2 + 1/x + O(x**(-6), (x, oo))
    assert acot(x + I).series(x, -oo) == 16/(5*x**5) + 2*I/x**4 - 4/(3*x**3) - I/x**2 + 1/x + O(x**(-6), (x, -oo))
    assert acot(x - I).series(x, oo) == 16/(5*x**5) - 2*I/x**4 - 4/(3*x**3) + I/x**2 + 1/x + O(x**(-6), (x, oo))
    assert acot(x - I).series(x, -oo) == 16/(5*x**5) - 2*I/x**4 - 4/(3*x**3) + I/x**2 + 1/x + O(x**(-6), (x, -oo))

