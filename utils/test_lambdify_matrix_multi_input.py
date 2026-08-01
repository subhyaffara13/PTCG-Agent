
def test_lambdify_matrix_multi_input():
    M = sympy.Matrix([[x**2, x*y, x*z],
                      [y*x, y**2, y*z],
                      [z*x, z*y, z**2]])
    f = lambdify((x, y, z), M, [{'ImmutableMatrix': numpy.array}, "numpy"])

    xh, yh, zh = 1.0, 2.0, 3.0
    expected = array([[xh**2, xh*yh, xh*zh],
                      [yh*xh, yh**2, yh*zh],
                      [zh*xh, zh*yh, zh**2]])
    actual = f(xh, yh, zh)
    assert numpy.allclose(actual, expected)

