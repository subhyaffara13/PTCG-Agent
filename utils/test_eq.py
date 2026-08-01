
def test_eq():
    assert Hyper_Function([1], []) == Hyper_Function([1], [])
    assert (Hyper_Function([1], []) != Hyper_Function([1], [])) is False
    assert Hyper_Function([1], []) != Hyper_Function([2], [])
    assert Hyper_Function([1], []) != Hyper_Function([1, 2], [])
    assert Hyper_Function([1], []) != Hyper_Function([1], [2])


def test_eq():
    # simple test
    assert 10*m == 10*m
    assert 10*m != 10*s


def test_eq():
    a = [[1, 2, 0, 3, 4, 5], [1, 0, 2, 3, 4, 5], [2, 1, 0, 3, 4, 5], [
        1, 2, 0, 3, 4, 5]]
    a = [Permutation(p) for p in a + [[1, 2, 3, 4, 5, 0]]]
    g = Permutation([1, 2, 3, 4, 5, 0])
    G1, G2, G3 = [PermutationGroup(x) for x in [a[:2], a[2:4], [g, g**2]]]
    assert G1.order() == G2.order() == G3.order() == 6
    assert G1.is_subgroup(G2)
    assert not G1.is_subgroup(G3)
    G4 = PermutationGroup([Permutation([0, 1])])
    assert not G1.is_subgroup(G4)
    assert G4.is_subgroup(G1, 0)
    assert PermutationGroup(g, g).is_subgroup(PermutationGroup(g))
    assert SymmetricGroup(3).is_subgroup(SymmetricGroup(4), 0)
    assert SymmetricGroup(3).is_subgroup(SymmetricGroup(3)*CyclicGroup(5), 0)
    assert not CyclicGroup(5).is_subgroup(SymmetricGroup(3)*CyclicGroup(5), 0)
    assert CyclicGroup(3).is_subgroup(SymmetricGroup(3)*CyclicGroup(5), 0)


def test_eq(same_matrix):
    sp_sparse, pd_sparse = same_matrix
    # temporary splint until pydata sparse support sparray equality
    sp_sparse = sp.coo_matrix(sp_sparse).asformat(sp_sparse.format)
    assert (sp_sparse == pd_sparse).all()

