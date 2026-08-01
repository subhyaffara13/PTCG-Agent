
def test_bbox_is_finite():
    assert not Bbox([(1, 1), (1, 1)])._is_finite()
    assert not Bbox([(0, 0), (np.inf, 1)])._is_finite()
    assert not Bbox([(-np.inf, 0), (2, 2)])._is_finite()
    assert not Bbox([(np.nan, 0), (2, 2)])._is_finite()
    assert Bbox([(0, 0), (0, 2)])._is_finite()
    assert Bbox([(0, 0), (2, 0)])._is_finite()
    assert Bbox([(0, 0), (1, 2)])._is_finite()

