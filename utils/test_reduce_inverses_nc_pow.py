
def test_reduce_inverses_nc_pow():
    x, y = symbols("x y", commutative=True)
    Z = symbols("Z", commutative=False)
    assert simplify(2**Z * y**Z) == 2**Z * y**Z
    assert simplify(x**Z * y**Z) == x**Z * y**Z
    x, y = symbols("x y", positive=True)
    assert expand((x*y)**Z) == x**Z * y**Z
    assert simplify(x**Z * y**Z) == expand((x*y)**Z)

