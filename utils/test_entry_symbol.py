
def test_entry_symbol():
    from sympy.concrete import Sum
    assert MatPow(C, 0)[0, 0] == 1
    assert MatPow(C, 0)[0, 1] == 0
    assert MatPow(C, 1)[0, 0] == C[0, 0]
    assert isinstance(MatPow(C, 2)[0, 0], Sum)
    assert isinstance(MatPow(C, n)[0, 0], MatrixElement)

