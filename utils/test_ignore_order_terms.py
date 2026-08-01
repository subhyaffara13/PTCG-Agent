
def test_ignore_order_terms():
    eq = exp(x).series(x,0,3) + sin(y+x**3) - 1
    assert cse(eq) == ([], [sin(x**3 + y) + x + x**2/2 + O(x**3)])

