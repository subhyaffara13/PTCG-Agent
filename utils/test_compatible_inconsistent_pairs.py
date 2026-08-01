
def test_compatible_inconsistent_pairs(idx1, idx2):
    # GH 23525
    res1 = idx1.union(idx2)
    res2 = idx2.union(idx1)

    assert res1.dtype in (idx1.dtype, idx2.dtype)
    assert res2.dtype in (idx1.dtype, idx2.dtype)

