
def test_derived_series():
    # the derived series of the trivial group consists only of the trivial group
    triv = PermutationGroup([Permutation([0, 1, 2])])
    assert triv.derived_series()[0].is_subgroup(triv)
    # the derived series for a simple group consists only of the group itself
    for i in (5, 6, 7):
        A = AlternatingGroup(i)
        assert A.derived_series()[0].is_subgroup(A)
    # the derived series for S_4 is S_4 > A_4 > K_4 > triv
    S = SymmetricGroup(4)
    series = S.derived_series()
    assert series[1].is_subgroup(AlternatingGroup(4))
    assert series[2].is_subgroup(DihedralGroup(2))
    assert series[3].is_trivial

