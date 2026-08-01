
def test_orbit_rep():
    G = DihedralGroup(6)
    assert G.orbit_rep(1, 3) in [Permutation([2, 3, 4, 5, 0, 1]),
    Permutation([4, 3, 2, 1, 0, 5])]
    H = CyclicGroup(4)*G
    assert H.orbit_rep(1, 5) is False

