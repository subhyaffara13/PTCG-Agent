
def test_replace_map():
    F, G = symbols('F, G', cls=Function)
    K = OperationsOnlyMatrix(2, 2, [(G(0), {F(0): G(0)}), (G(1), {F(1): G(1)}), (G(1), {F(1) \
                                                                              : G(1)}), (G(2), {F(2): G(2)})])
    M = OperationsOnlyMatrix(2, 2, lambda i, j: F(i+j))
    N = M.replace(F, G, True)
    assert N == K


def test_replace_map():
    F, G = symbols('F, G', cls=Function)
    M = Matrix(2, 2, lambda i, j: F(i+j))
    N, d = M.replace(F, G, True)
    assert N == Matrix(2, 2, lambda i, j: G(i+j))
    assert d == {F(0): G(0), F(1): G(1), F(2): G(2)}

