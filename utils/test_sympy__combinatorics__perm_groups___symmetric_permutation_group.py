
def test_sympy__combinatorics__perm_groups__SymmetricPermutationGroup():
    from sympy.combinatorics.perm_groups import SymmetricPermutationGroup
    assert _test_args(SymmetricPermutationGroup(5))

