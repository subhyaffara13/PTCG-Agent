
def test_sympy__tensor__functions__TensorProduct():
    from sympy.tensor.functions import TensorProduct
    A = MatrixSymbol('A', 3, 3)
    B = MatrixSymbol('B', 3, 3)
    tp = TensorProduct(A, B)
    assert _test_args(tp)

