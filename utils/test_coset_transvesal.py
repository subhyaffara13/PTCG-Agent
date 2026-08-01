
def test_coset_transvesal():
    G = AlternatingGroup(5)
    H = PermutationGroup(Permutation(0,1,2),Permutation(1,2)(3,4))
    assert G.coset_transversal(H) == \
        [Permutation(4), Permutation(2, 3, 4), Permutation(2, 4, 3),
         Permutation(1, 2, 4), Permutation(4)(1, 2, 3), Permutation(1, 3)(2, 4),
         Permutation(0, 1, 2, 3, 4), Permutation(0, 1, 2, 4, 3),
         Permutation(0, 1, 3, 2, 4), Permutation(0, 2, 4, 1, 3)]

