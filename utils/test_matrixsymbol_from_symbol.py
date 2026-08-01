
def test_matrixsymbol_from_symbol():
    # The label should be preserved during doit and subs
    A_label = Symbol('A', complex=True)
    A = MatrixSymbol(A_label, 2, 2)

    A_1 = A.doit()
    A_2 = A.subs(2, 3)
    assert A_1.args == A.args
    assert A_2.args[0] == A.args[0]

