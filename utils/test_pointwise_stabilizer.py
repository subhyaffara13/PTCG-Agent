
def test_pointwise_stabilizer():
    S = SymmetricGroup(2)
    stab = S.pointwise_stabilizer([0])
    assert stab.generators == [Permutation(1)]
    S = SymmetricGroup(5)
    points = []
    stab = S
    for point in (2, 0, 3, 4, 1):
        stab = stab.stabilizer(point)
        points.append(point)
        assert S.pointwise_stabilizer(points).is_subgroup(stab)

