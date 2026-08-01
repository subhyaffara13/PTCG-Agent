
def runtest_ufuncify(language, backend):
    has_module('numpy')
    a, b, c = symbols('a b c')
    fabc = ufuncify([a, b, c], a*b + c, backend=backend)
    facb = ufuncify([a, c, b], a*b + c, backend=backend)
    grid = numpy.linspace(-2, 2, 50)
    b = numpy.linspace(-5, 4, 50)
    c = numpy.linspace(-1, 1, 50)
    expected = grid*b + c
    numpy.testing.assert_allclose(fabc(grid, b, c), expected)
    numpy.testing.assert_allclose(facb(grid, c, b), expected)

