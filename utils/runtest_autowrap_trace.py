
def runtest_autowrap_trace(language, backend):
    has_module('numpy')
    trace = autowrap(A[i, i], language, backend)
    assert trace(numpy.eye(100)) == 100

