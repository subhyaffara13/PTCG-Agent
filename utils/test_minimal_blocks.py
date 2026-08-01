
def test_minimal_blocks():
    P = PermutationGroup(Permutation(1, 5)(2, 4), Permutation(0, 1, 2, 3, 4, 5))
    assert P.minimal_blocks() == [[0, 1, 0, 1, 0, 1], [0, 1, 2, 0, 1, 2]]

    P = SymmetricGroup(5)
    assert P.minimal_blocks() == [[0]*5]

    P = PermutationGroup(Permutation(0, 3))
    assert P.minimal_blocks() is False

