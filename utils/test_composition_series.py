
def test_composition_series():
    a = Permutation(1, 2, 3)
    b = Permutation(1, 2)
    G = PermutationGroup([a, b])
    comp_series = G.composition_series()
    assert comp_series == G.derived_series()
    # The first group in the composition series is always the group itself and
    # the last group in the series is the trivial group.
    S = SymmetricGroup(4)
    assert S.composition_series()[0] == S
    assert len(S.composition_series()) == 5
    A = AlternatingGroup(4)
    assert A.composition_series()[0] == A
    assert len(A.composition_series()) == 4

    # the composition series for C_8 is C_8 > C_4 > C_2 > triv
    G = CyclicGroup(8)
    series = G.composition_series()
    assert is_isomorphic(series[1], CyclicGroup(4))
    assert is_isomorphic(series[2], CyclicGroup(2))
    assert series[3].is_trivial

