
def test_TensorProduct_printing():
    from sympy.tensor.functions import TensorProduct
    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)
    assert latex(TensorProduct(A, B)) == r"A \otimes B"

