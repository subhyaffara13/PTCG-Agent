
def test_subgroup():
    G = PermutationGroup(Permutation(0,1,2), Permutation(0,2,3))
    H = G.subgroup([Permutation(0,1,3)])
    assert H.is_subgroup(G)

