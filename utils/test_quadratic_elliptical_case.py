
def test_quadratic_elliptical_case():
    # Elliptical case: B**2 - 4AC < 0

    assert diop_solve(42*x**2 + 8*x*y + 15*y**2 + 23*x + 17*y - 4915) == {(-11, -1)}
    assert diop_solve(4*x**2 + 3*y**2 + 5*x - 11*y + 12) == set()
    assert diop_solve(x**2 + y**2 + 2*x + 2*y + 2) == {(-1, -1)}
    assert diop_solve(15*x**2 - 9*x*y + 14*y**2 - 23*x - 14*y - 4950) == {(-15, 6)}
    assert diop_solve(10*x**2 + 12*x*y + 12*y**2 - 34) == \
           {(-1, -1), (-1, 2), (1, -2), (1, 1)}

