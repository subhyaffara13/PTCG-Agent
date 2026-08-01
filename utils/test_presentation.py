
def test_presentation():
    def _test(P):
        G = P.presentation()
        return G.order() == P.order()

    def _strong_test(P):
        G = P.strong_presentation()
        chk = len(G.generators) == len(P.strong_gens)
        return chk and G.order() == P.order()

    P = PermutationGroup(Permutation(0,1,5,2)(3,7,4,6), Permutation(0,3,5,4)(1,6,2,7))
    assert _test(P)

    P = AlternatingGroup(5)
    assert _test(P)

    P = SymmetricGroup(5)
    assert _test(P)

    P = PermutationGroup(
        [Permutation(0,3,1,2), Permutation(3)(0,1), Permutation(0,1)(2,3)])
    assert _strong_test(P)

    P = DihedralGroup(6)
    assert _strong_test(P)

    a = Permutation(0,1)(2,3)
    b = Permutation(0,2)(3,1)
    c = Permutation(4,5)
    P = PermutationGroup(c, a, b)
    assert _strong_test(P)

