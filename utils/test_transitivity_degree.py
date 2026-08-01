
def test_transitivity_degree():
    perm = Permutation([1, 2, 0])
    C = PermutationGroup([perm])
    assert C.transitivity_degree == 1
    gen1 = Permutation([1, 2, 0, 3, 4])
    gen2 = Permutation([1, 2, 3, 4, 0])
    # alternating group of degree 5
    Alt = PermutationGroup([gen1, gen2])
    assert Alt.transitivity_degree == 3

