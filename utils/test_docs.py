
def test_docs(doc):
    assert (
        doc(m.vectorized_func)
        == """
        vectorized_func(arg0: numpy.ndarray[numpy.int32], arg1: numpy.ndarray[numpy.float32], arg2: numpy.ndarray[numpy.float64]) -> object
    """
    )


def test_docs():
    f = lambdify(x, x**2)
    assert f(2) == 4
    f = lambdify([x, y, z], [z, y, x])
    assert f(1, 2, 3) == [3, 2, 1]
    f = lambdify(x, sqrt(x))
    assert f(4) == 2.0
    f = lambdify((x, y), sin(x*y)**2)
    assert f(0, 5) == 0

