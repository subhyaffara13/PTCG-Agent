
def test_PolyElement_shift():
    _, x = ring("x", ZZ)
    assert (x**2 - 2*x + 1).shift(2) == x**2 + 2*x + 1
    assert (x**2 - 2*x + 1).shift_list([2]) == x**2 + 2*x + 1

    R, x, y = ring("x, y", ZZ)
    assert (x*y).shift_list([1, 2]) == (x+1)*(y+2)

    raises(MultivariatePolynomialError, lambda: (x*y).shift(1))

