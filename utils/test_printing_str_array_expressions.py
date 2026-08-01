
def test_printing_str_array_expressions():
    assert sstr(ArraySymbol("A", (2, 3, 4))) == "A"
    assert sstr(ArrayElement("A", (2, 1/(1-x), 0))) == "A[2, 1/(1 - x), 0]"
    M = MatrixSymbol("M", 3, 3)
    N = MatrixSymbol("N", 3, 3)
    assert sstr(ArrayElement(M*N, [x, 0])) == "(M*N)[x, 0]"

