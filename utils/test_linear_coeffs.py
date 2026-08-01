
def test_linear_coeffs():
    from sympy.solvers.solveset import linear_coeffs
    assert linear_coeffs(0, x) == [0, 0]
    assert all(i is S.Zero for i in linear_coeffs(0, x))
    assert linear_coeffs(x + 2*y + 3, x, y) == [1, 2, 3]
    assert linear_coeffs(x + 2*y + 3, y, x) == [2, 1, 3]
    assert linear_coeffs(x + 2*x**2 + 3, x, x**2) == [1, 2, 3]
    raises(ValueError, lambda:
        linear_coeffs(x + 2*x**2 + x**3, x, x**2))
    raises(ValueError, lambda:
        linear_coeffs(1/x*(x - 1) + 1/x, x))
    raises(ValueError, lambda:
        linear_coeffs(x, x, x))
    assert linear_coeffs(a*(x + y), x, y) == [a, a, 0]
    assert linear_coeffs(1.0, x, y) == [0, 0, 1.0]
    # don't include coefficients of 0
    assert linear_coeffs(Eq(x, x + y), x, y, dict=True) == {y: -1}
    assert linear_coeffs(0, x, y, dict=True) == {}

