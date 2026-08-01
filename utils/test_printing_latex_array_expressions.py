
def test_printing_latex_array_expressions():
    assert latex(ArraySymbol("A", (2, 3, 4))) == "A"
    assert latex(ArrayElement("A", (2, 1/(1-x), 0))) == "{{A}_{2, \\frac{1}{1 - x}, 0}}"
    M = MatrixSymbol("M", 3, 3)
    N = MatrixSymbol("N", 3, 3)
    assert latex(ArrayElement(M*N, [x, 0])) == "{{\\left(M N\\right)}_{x, 0}}"

