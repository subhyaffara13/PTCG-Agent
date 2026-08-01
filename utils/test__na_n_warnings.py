
def test_NaN_warnings():
    with warnings.catch_warnings(record=True) as record:
        shortest_path(np.array([[0, 1], [np.nan, 0]]))
    for r in record:
        assert r.category is not RuntimeWarning

