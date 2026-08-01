
def test_issue_15827():
    if not numpy:
        skip("numpy not installed")
    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 2, 3)
    C = MatrixSymbol("C", 3, 4)
    D = MatrixSymbol("D", 4, 5)
    k=symbols("k")
    f = lambdify(A, (2*k)*A)
    g = lambdify(A, (2+k)*A)
    h = lambdify(A, 2*A)
    i = lambdify((B, C, D), 2*B*C*D)
    assert numpy.array_equal(f(numpy.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])), \
    numpy.array([[2*k, 4*k, 6*k], [2*k, 4*k, 6*k], [2*k, 4*k, 6*k]], dtype=object))

    assert numpy.array_equal(g(numpy.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])), \
    numpy.array([[k + 2, 2*k + 4, 3*k + 6], [k + 2, 2*k + 4, 3*k + 6], \
    [k + 2, 2*k + 4, 3*k + 6]], dtype=object))

    assert numpy.array_equal(h(numpy.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])), \
    numpy.array([[2, 4, 6], [2, 4, 6], [2, 4, 6]]))

    assert numpy.array_equal(i(numpy.array([[1, 2, 3], [1, 2, 3]]), numpy.array([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]), \
    numpy.array([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])), numpy.array([[ 120, 240, 360, 480, 600], \
    [ 120, 240, 360, 480, 600]]))

