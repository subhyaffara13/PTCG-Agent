
def runtest_autowrap_matrix_vector(language, backend):
    has_module('numpy')
    x, y = symbols('x y', cls=IndexedBase)
    expr = Eq(y[i], A[i, j]*x[j])
    mv = autowrap(expr, language, backend)

    # compare with numpy's dot product
    M = numpy.random.rand(10, 20)
    x = numpy.random.rand(20)
    y = numpy.dot(M, x)
    assert numpy.sum(numpy.abs(y - mv(M, x))) < 1e-13

