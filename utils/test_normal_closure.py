
def test_normal_closure():
    # the normal closure of the trivial group is trivial
    S = SymmetricGroup(3)
    identity = Permutation([0, 1, 2])
    closure = S.normal_closure(identity)
    assert closure.is_trivial
    # the normal closure of the entire group is the entire group
    A = AlternatingGroup(4)
    assert A.normal_closure(A).is_subgroup(A)
    # brute-force verifications for subgroups
    for i in (3, 4, 5):
        S = SymmetricGroup(i)
        A = AlternatingGroup(i)
        D = DihedralGroup(i)
        C = CyclicGroup(i)
        for gp in (A, D, C):
            assert _verify_normal_closure(S, gp)
    # brute-force verifications for all elements of a group
    S = SymmetricGroup(5)
    elements = list(S.generate_dimino())
    for element in elements:
        assert _verify_normal_closure(S, element)
    # small groups
    small = []
    for i in (1, 2, 3):
        small.append(SymmetricGroup(i))
        small.append(AlternatingGroup(i))
        small.append(DihedralGroup(i))
        small.append(CyclicGroup(i))
    for gp in small:
        for gp2 in small:
            if gp2.is_subgroup(gp, 0) and gp2.degree == gp.degree:
                assert _verify_normal_closure(gp, gp2)

