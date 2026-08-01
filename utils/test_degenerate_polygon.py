
def test_degenerate_polygon():
    point = [0, 0]
    correct_extents = Bbox([point, point]).extents
    assert np.all(Polygon([point]).get_extents().extents == correct_extents)

