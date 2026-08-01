
def test_nan_overlap():
    a = mtransforms.Bbox([[0, 0], [1, 1]])
    b = mtransforms.Bbox([[0, 0], [1, np.nan]])
    assert not a.overlaps(b)

