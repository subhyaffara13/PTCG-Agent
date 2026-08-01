
def test_sympy__matrices__expressions__permutation__PermutationMatrix():
    from sympy.combinatorics import Permutation
    from sympy.matrices.expressions.permutation import PermutationMatrix
    assert _test_args(PermutationMatrix(Permutation([2, 0, 1])))

