
def test_elements():
    from sympy.sets.sets import FiniteSet

    p = Permutation(2, 3)
    assert set(PermutationGroup(p).elements) == {Permutation(3), Permutation(2, 3)}
    assert FiniteSet(*PermutationGroup(p).elements) \
        == FiniteSet(Permutation(2, 3), Permutation(3))

