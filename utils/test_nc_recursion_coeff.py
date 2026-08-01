
def test_nc_recursion_coeff():
    X = symbols("X", commutative = False)
    assert (2 * cos(pi/3) * X).simplify() == X
    assert (2.0 * cos(pi/3) * X).simplify() == X

