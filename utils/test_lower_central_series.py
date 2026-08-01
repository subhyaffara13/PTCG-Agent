
def test_lower_central_series():
    # the lower central series of the trivial group consists of the trivial
    # group
    triv = PermutationGroup([Permutation([0, 1, 2])])
    assert triv.lower_central_series()[0].is_subgroup(triv)
    # the lower central series of a simple group consists of the group itself
    for i in (5, 6, 7):
        A = AlternatingGroup(i)
        assert A.lower_central_series()[0].is_subgroup(A)
    # GAP-verified example
    S = SymmetricGroup(6)
    series = S.lower_central_series()
    assert len(series) == 2
    assert series[1].is_subgroup(AlternatingGroup(6))

