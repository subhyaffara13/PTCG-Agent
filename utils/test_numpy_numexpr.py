
def test_numpy_numexpr():
    if not numpy:
        skip("numpy not installed.")
    if not numexpr:
        skip("numexpr not installed.")
    a, b, c = numpy.random.randn(3, 128, 128)
    # ensure that numpy and numexpr return same value for complicated expression
    expr = sin(x) + cos(y) + tan(z)**2 + Abs(z-y)*acos(sin(y*z)) + \
           Abs(y-z)*acosh(2+exp(y-x))- sqrt(x**2+I*y**2)
    npfunc = lambdify((x, y, z), expr, modules='numpy')
    nefunc = lambdify((x, y, z), expr, modules='numexpr')
    assert numpy.allclose(npfunc(a, b, c), nefunc(a, b, c))

