
def test_sympy__combinatorics__permutations__AppliedPermutation():
    from sympy.combinatorics.permutations import Permutation
    from sympy.combinatorics.permutations import AppliedPermutation
    p = Permutation([0, 1, 2, 3])
    assert _test_args(AppliedPermutation(p, x))

