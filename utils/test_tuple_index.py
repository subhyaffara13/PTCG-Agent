
def test_tuple_index():
    # GH 35534 - Selecting values when a Series has an Index of tuples
    s = Series([1, 2], index=[("a",), ("b",)])
    assert s[("a",)] == 1
    assert s[("b",)] == 2
    s[("b",)] = 3
    assert s[("b",)] == 3


def test_tuple_index(temp_h5_path, performance_warning):
    # GH #492
    col = np.arange(10)
    idx = [(0.0, 1.0), (2.0, 3.0), (4.0, 5.0)]
    data = np.random.default_rng(2).standard_normal(30).reshape((3, 10))
    DF = DataFrame(data, index=idx, columns=col)

    with tm.assert_produces_warning(performance_warning):
        _check_roundtrip(DF, tm.assert_frame_equal, path=temp_h5_path)

