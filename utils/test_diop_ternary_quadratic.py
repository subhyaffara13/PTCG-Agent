
def test_diop_ternary_quadratic():
    assert check_solutions(2*x**2 + z**2 + y**2 - 4*x*y)
    assert check_solutions(x**2 - y**2 - z**2 - x*y - y*z)
    assert check_solutions(3*x**2 - x*y - y*z - x*z)
    assert check_solutions(x**2 - y*z - x*z)
    assert check_solutions(5*x**2 - 3*x*y - x*z)
    assert check_solutions(4*x**2 - 5*y**2 - x*z)
    assert check_solutions(3*x**2 + 2*y**2 - z**2 - 2*x*y + 5*y*z - 7*y*z)
    assert check_solutions(8*x**2 - 12*y*z)
    assert check_solutions(45*x**2 - 7*y**2 - 8*x*y - z**2)
    assert check_solutions(x**2 - 49*y**2 - z**2 + 13*z*y -8*x*y)
    assert check_solutions(90*x**2 + 3*y**2 + 5*x*y + 2*z*y + 5*x*z)
    assert check_solutions(x**2 + 3*y**2 + z**2 - x*y - 17*y*z)
    assert check_solutions(x**2 + 3*y**2 + z**2 - x*y - 16*y*z + 12*x*z)
    assert check_solutions(x**2 + 3*y**2 + z**2 - 13*x*y - 16*y*z + 12*x*z)
    assert check_solutions(x*y - 7*y*z + 13*x*z)

    assert diop_ternary_quadratic_normal(x**2 + y**2 + z**2) == (None, None, None)
    assert diop_ternary_quadratic_normal(x**2 + y**2) is None
    raises(ValueError, lambda:
        _diop_ternary_quadratic_normal((x, y, z),
        {x*y: 1, x**2: 2, y**2: 3, z**2: 0}))
    eq = -2*x*y - 6*x*z + 7*y**2 - 3*y*z + 4*z**2
    assert diop_ternary_quadratic(eq) == (7, 2, 0)
    assert diop_ternary_quadratic_normal(4*x**2 + 5*y**2 - z**2) == \
        (1, 0, 2)
    assert diop_ternary_quadratic(x*y + 2*y*z) == \
        (-2, 0, n1)
    eq = -5*x*y - 8*x*z - 3*y*z + 8*z**2
    assert parametrize_ternary_quadratic(eq) == \
        (8*p**2 - 3*p*q, -8*p*q + 8*q**2, 5*p*q)
    # this cannot be tested with diophantine because it will
    # factor into a product
    assert diop_solve(x*y + 2*y*z) == (-2*p*q, -n1*p**2 + p**2, p*q)

