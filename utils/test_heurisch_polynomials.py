
def test_heurisch_polynomials():
    assert heurisch(1, x) == x
    assert heurisch(x, x) == x**2/2
    assert heurisch(x**17, x) == x**18/18
    # For coverage
    assert heurisch_wrapper(y, x) == y*x

