
def test_group_no_duplicates(name, size):
    g = Rotation.create_group(name)
    kdtree = cKDTree(g.as_quat())
    assert len(kdtree.query_pairs(1E-3)) == 0

