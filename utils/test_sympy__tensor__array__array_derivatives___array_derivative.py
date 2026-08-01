
def test_sympy__tensor__array__array_derivatives__ArrayDerivative():
    from sympy.tensor.array.array_derivatives import ArrayDerivative
    A = MatrixSymbol("A", 2, 2)
    arrder = ArrayDerivative(A, A, evaluate=False)
    assert _test_args(arrder)

