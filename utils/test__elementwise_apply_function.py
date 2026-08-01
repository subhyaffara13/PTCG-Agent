
def test_ElementwiseApplyFunction():
    X = MatrixSymbol('X', 2, 2)
    expr = (X.T*X).applyfunc(sin)
    assert latex(expr) == r"{\left( d \mapsto \sin{\left(d \right)} \right)}_{\circ}\left({X^{T} X}\right)"
    expr = X.applyfunc(Lambda(x, 1/x))
    assert latex(expr) == r'{\left( x \mapsto \frac{1}{x} \right)}_{\circ}\left({X}\right)'

