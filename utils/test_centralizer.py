
def test_centralizer():
    # the centralizer of the trivial group is the entire group
    S = SymmetricGroup(2)
    assert S.centralizer(Permutation(list(range(2)))).is_subgroup(S)
    A = AlternatingGroup(5)
    assert A.centralizer(Permutation(list(range(5)))).is_subgroup(A)
    # a centralizer in the trivial group is the trivial group itself
    triv = PermutationGroup([Permutation([0, 1, 2, 3])])
    D = DihedralGroup(4)
    assert triv.centralizer(D).is_subgroup(triv)
    # brute-force verifications for centralizers of groups
    for i in (4, 5, 6):
        S = SymmetricGroup(i)
        A = AlternatingGroup(i)
        C = CyclicGroup(i)
        D = DihedralGroup(i)
        for gp in (S, A, C, D):
            for gp2 in (S, A, C, D):
                if not gp2.is_subgroup(gp):
                    assert _verify_centralizer(gp, gp2)
    # verify the centralizer for all elements of several groups
    S = SymmetricGroup(5)
    elements = list(S.generate_dimino())
    for element in elements:
        assert _verify_centralizer(S, element)
    A = AlternatingGroup(5)
    elements = list(A.generate_dimino())
    for element in elements:
        assert _verify_centralizer(A, element)
    D = DihedralGroup(7)
    elements = list(D.generate_dimino())
    for element in elements:
        assert _verify_centralizer(D, element)
    # verify centralizers of small groups within small groups
    small = []
    for i in (1, 2, 3):
        small.append(SymmetricGroup(i))
        small.append(AlternatingGroup(i))
        small.append(DihedralGroup(i))
        small.append(CyclicGroup(i))
    for gp in small:
        for gp2 in small:
            if gp.degree == gp2.degree:
                assert _verify_centralizer(gp, gp2)

