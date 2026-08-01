
def test_pretty_dotproduct():
    from sympy.matrices.expressions.dotproduct import DotProduct
    n = symbols("n", integer=True)
    A = MatrixSymbol('A', n, 1)
    B = MatrixSymbol('B', n, 1)
    C = Matrix(1, 3, [1, 2, 3])
    D = Matrix(1, 3, [1, 3, 4])

    assert pretty(DotProduct(A, B)) == "A*B"
    assert pretty(DotProduct(C, D)) == "[1  2  3]*[1  3  4]"
    assert upretty(DotProduct(A, B)) == "A⋅B"
    assert upretty(DotProduct(C, D)) == "[1  2  3]⋅[1  3  4]"

