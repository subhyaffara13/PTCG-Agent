
def test_series2x():
    assert ((x + 1)**(-2)).nseries(x, 0, 4) == 1 - 2*x + 3*x**2 - 4*x**3 + O(x**4, x)
    assert ((x + 1)**(-1)).nseries(x, 0, 4) == 1 - x + x**2 - x**3 + O(x**4, x)
    assert ((x + 1)**0).nseries(x, 0, 3) == 1
    assert ((x + 1)**1).nseries(x, 0, 3) == 1 + x
    assert ((x + 1)**2).nseries(x, 0, 3) == x**2 + 2*x + 1
    assert ((x + 1)**3).nseries(x, 0, 3) == 1 + 3*x + 3*x**2 + O(x**3)

    assert (1/(1 + x)).nseries(x, 0, 4) == 1 - x + x**2 - x**3 + O(x**4, x)
    assert (x + 3/(1 + 2*x)).nseries(x, 0, 4) == 3 - 5*x + 12*x**2 - 24*x**3 + O(x**4, x)

    assert ((1/x + 1)**3).nseries(x, 0, 3) == 1 + 3/x + 3/x**2 + x**(-3)
    assert (1/(1 + 1/x)).nseries(x, 0, 4) == x - x**2 + x**3 - O(x**4, x)
    assert (1/(1 + 1/x**2)).nseries(x, 0, 6) == x**2 - x**4 + O(x**6, x)

