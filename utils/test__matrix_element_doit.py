
def test_MatrixElement_doit():
    u = MatrixSymbol('u', 2, 1)
    v = ImmutableMatrix([3, 5])
    assert u[0, 0].subs(u, v).doit() == v[0, 0]

