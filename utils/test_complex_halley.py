
def test_complex_halley():
    """Test Halley's works with complex roots"""
    def f(x, *a):
        return a[0] * x**2 + a[1] * x + a[2]

    def f_1(x, *a):
        return 2 * a[0] * x + a[1]

    def f_2(x, *a):
        retval = 2 * a[0]
        try:
            size = len(x)
        except TypeError:
            return retval
        else:
            return [retval] * size

    z = complex(1.0, 2.0)
    coeffs = (2.0, 3.0, 4.0)
    y = zeros.newton(f, z, args=coeffs, fprime=f_1, fprime2=f_2, tol=1e-6)
    # (-0.75000000000000078+1.1989578808281789j)
    assert_allclose(f(y, *coeffs), 0, atol=1e-6)
    z = [z] * 10
    coeffs = (2.0, 3.0, 4.0)
    y = zeros.newton(f, z, args=coeffs, fprime=f_1, fprime2=f_2, tol=1e-6)
    assert_allclose(f(y, *coeffs), 0, atol=1e-6)

