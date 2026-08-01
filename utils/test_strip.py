
def test_strip():
    D = DihedralGroup(5)
    D.schreier_sims()
    member = Permutation([4, 0, 1, 2, 3])
    not_member1 = Permutation([0, 1, 4, 3, 2])
    not_member2 = Permutation([3, 1, 4, 2, 0])
    identity = Permutation([0, 1, 2, 3, 4])
    res1 = _strip(member, D.base, D.basic_orbits, D.basic_transversals)
    res2 = _strip(not_member1, D.base, D.basic_orbits, D.basic_transversals)
    res3 = _strip(not_member2, D.base, D.basic_orbits, D.basic_transversals)
    assert res1[0] == identity
    assert res1[1] == len(D.base) + 1
    assert res2[0] == not_member1
    assert res2[1] == len(D.base) + 1
    assert res3[0] != identity
    assert res3[1] == 2

