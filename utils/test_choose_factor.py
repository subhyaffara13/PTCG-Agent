
def test_choose_factor():
    # Test that this does not enter an infinite loop:
    bad_factors = [Poly(x-2, x), Poly(x+2, x)]
    raises(NotImplementedError, lambda: _choose_factor(bad_factors, x, sqrt(3)))

