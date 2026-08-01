
def test_check_homomorphism():
    a = Permutation(1,2,3,4)
    b = Permutation(1,3)
    G = PermutationGroup([a, b])
    raises(ValueError, lambda: homomorphism(G, G, [a], [a]))

