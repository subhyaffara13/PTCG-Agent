
def test_TransferFunction_printing():
    tf1 = TransferFunction(x - 1, x + 1, x)
    assert latex(tf1) == r"\frac{x - 1}{x + 1}"
    tf2 = TransferFunction(x + 1, 2 - y, x)
    assert latex(tf2) == r"\frac{x + 1}{2 - y}"
    tf3 = TransferFunction(y, y**2 + 2*y + 3, y)
    assert latex(tf3) == r"\frac{y}{y^{2} + 2 y + 3}"

