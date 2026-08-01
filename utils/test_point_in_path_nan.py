
def test_point_in_path_nan():
    box = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    p = Path(box)
    test = np.array([[np.nan, 0.5]])
    contains = p.contains_points(test)
    assert len(contains) == 1
    assert not contains[0]

