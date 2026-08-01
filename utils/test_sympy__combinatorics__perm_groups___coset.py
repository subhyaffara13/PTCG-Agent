
def test_sympy__combinatorics__perm_groups__Coset():
    from sympy.combinatorics.permutations import Permutation
    from sympy.combinatorics.perm_groups import PermutationGroup, Coset
    a = Permutation(1, 2)
    b = Permutation(0, 1)
    G = PermutationGroup([a, b])
    assert _test_args(Coset(a, G))

