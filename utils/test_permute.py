
def test_permute():
    A, B, C, D, E, F, G = symbols('A B C D E F G', commutative=False)
    t = Tr(A*B*C*D*E*F*G)

    assert t.permute(0).args[0].args == (A, B, C, D, E, F, G)
    assert t.permute(2).args[0].args == (F, G, A, B, C, D, E)
    assert t.permute(4).args[0].args == (D, E, F, G, A, B, C)
    assert t.permute(6).args[0].args == (B, C, D, E, F, G, A)
    assert t.permute(8).args[0].args == t.permute(1).args[0].args

    assert t.permute(-1).args[0].args == (B, C, D, E, F, G, A)
    assert t.permute(-3).args[0].args == (D, E, F, G, A, B, C)
    assert t.permute(-5).args[0].args == (F, G, A, B, C, D, E)
    assert t.permute(-8).args[0].args == t.permute(-1).args[0].args

    t = Tr((A + B)*(B*B)*C*D)
    assert t.permute(2).args[0].args == (C, D, (A + B), (B**2))

    t1 = Tr(A*B)
    t2 = t1.permute(1)
    assert id(t1) != id(t2) and t1 == t2


def test_permute():
    a = OperationsOnlyMatrix(3, 4, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    raises(IndexError, lambda: a.permute([[0, 5]]))
    raises(ValueError, lambda: a.permute(Symbol('x')))
    b = a.permute_rows([[0, 2], [0, 1]])
    assert a.permute([[0, 2], [0, 1]]) == b == Matrix([
                                            [5,  6,  7,  8],
                                            [9, 10, 11, 12],
                                            [1,  2,  3,  4]])

    b = a.permute_cols([[0, 2], [0, 1]])
    assert a.permute([[0, 2], [0, 1]], orientation='cols') == b ==\
                            Matrix([
                            [ 2,  3, 1,  4],
                            [ 6,  7, 5,  8],
                            [10, 11, 9, 12]])

    b = a.permute_cols([[0, 2], [0, 1]], direction='backward')
    assert a.permute([[0, 2], [0, 1]], orientation='cols', direction='backward') == b ==\
                            Matrix([
                            [ 3, 1,  2,  4],
                            [ 7, 5,  6,  8],
                            [11, 9, 10, 12]])

    assert a.permute([1, 2, 0, 3]) == Matrix([
                                            [5,  6,  7,  8],
                                            [9, 10, 11, 12],
                                            [1,  2,  3,  4]])

    from sympy.combinatorics import Permutation
    assert a.permute(Permutation([1, 2, 0, 3])) == Matrix([
                                            [5,  6,  7,  8],
                                            [9, 10, 11, 12],
                                            [1,  2,  3,  4]])


def test_permute():
    a = Matrix(3, 4, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    raises(IndexError, lambda: a.permute([[0, 5]]))
    raises(ValueError, lambda: a.permute(Symbol('x')))
    b = a.permute_rows([[0, 2], [0, 1]])
    assert a.permute([[0, 2], [0, 1]]) == b == Matrix([
                                            [5,  6,  7,  8],
                                            [9, 10, 11, 12],
                                            [1,  2,  3,  4]])

    b = a.permute_cols([[0, 2], [0, 1]])
    assert a.permute([[0, 2], [0, 1]], orientation='cols') == b ==\
                            Matrix([
                            [ 2,  3, 1,  4],
                            [ 6,  7, 5,  8],
                            [10, 11, 9, 12]])

    b = a.permute_cols([[0, 2], [0, 1]], direction='backward')
    assert a.permute([[0, 2], [0, 1]], orientation='cols', direction='backward') == b ==\
                            Matrix([
                            [ 3, 1,  2,  4],
                            [ 7, 5,  6,  8],
                            [11, 9, 10, 12]])

    assert a.permute([1, 2, 0, 3]) == Matrix([
                                            [5,  6,  7,  8],
                                            [9, 10, 11, 12],
                                            [1,  2,  3,  4]])

    from sympy.combinatorics import Permutation
    assert a.permute(Permutation([1, 2, 0, 3])) == Matrix([
                                            [5,  6,  7,  8],
                                            [9, 10, 11, 12],
                                            [1,  2,  3,  4]])

