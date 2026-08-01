
def test_16857():
    if not jax:
        skip("JAX not installed")

    a_1 = MatrixSymbol('a_1', 10, 3)
    a_2 = MatrixSymbol('a_2', 10, 3)
    a_3 = MatrixSymbol('a_3', 10, 3)
    a_4 = MatrixSymbol('a_4', 10, 3)
    A = BlockMatrix([[a_1, a_2], [a_3, a_4]])
    assert A.shape == (20, 6)

    printer = JaxPrinter()
    assert printer.doprint(A) == 'jax.numpy.block([[a_1, a_2], [a_3, a_4]])'


def test_16857():
    if not np:
        skip("NumPy not installed")

    a_1 = MatrixSymbol('a_1', 10, 3)
    a_2 = MatrixSymbol('a_2', 10, 3)
    a_3 = MatrixSymbol('a_3', 10, 3)
    a_4 = MatrixSymbol('a_4', 10, 3)
    A = BlockMatrix([[a_1, a_2], [a_3, a_4]])
    assert A.shape == (20, 6)

    printer = NumPyPrinter()
    assert printer.doprint(A) == 'numpy.block([[a_1, a_2], [a_3, a_4]])'

