
def test_assoc_legendre_numerical_evaluation():

    tol = 1e-10

    sympy_result_integer = assoc_legendre(1, 1/2, 0.1).evalf()
    sympy_result_complex = assoc_legendre(2, 1, 3).evalf()
    mpmath_result_integer = -0.474572528387641
    mpmath_result_complex = -25.45584412271571*I

    assert all_close(sympy_result_integer, mpmath_result_integer, tol)
    assert all_close(sympy_result_complex, mpmath_result_complex, tol)

