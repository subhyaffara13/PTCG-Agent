
def test_sympy__matrices__expressions__permutation__MatrixPermute():
    from sympy.combinatorics import Permutation
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    from sympy.matrices.expressions.permutation import MatrixPermute
    A = MatrixSymbol('A', 3, 3)
    assert _test_args(MatrixPermute(A, Permutation([2, 0, 1])))

