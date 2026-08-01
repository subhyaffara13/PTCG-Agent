
def test_OneMatrix_doit():
    n = symbols('n', integer=True)
    Unn = OneMatrix(Add(n, n, evaluate=False), n)
    assert isinstance(Unn.rows, Add)
    assert Unn.doit() == OneMatrix(2 * n, n)
    assert isinstance(Unn.doit().rows, Mul)

