
def test_geometric_1():
    assert (1/(1 - x)).nseries(x, n=5) == 1 + x + x**2 + x**3 + x**4 + O(x**5)
    assert (x/(1 - x)).nseries(x, n=6) == x + x**2 + x**3 + x**4 + x**5 + O(x**6)
    assert (x**3/(1 - x)).nseries(x, n=8) == x**3 + x**4 + x**5 + x**6 + \
        x**7 + O(x**8)

