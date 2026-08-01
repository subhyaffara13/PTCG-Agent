
def test_isin_empty():
    # GH#51599
    midx = MultiIndex.from_arrays([[1, 2], [3, 4]])
    result = midx.isin([])
    expected = np.array([False, False])
    tm.assert_numpy_array_equal(result, expected)


def test_isin_empty(empty):
    s = pd.Categorical(["a", "b"])
    expected = np.array([False, False], dtype=bool)

    result = s.isin(empty)
    tm.assert_numpy_array_equal(expected, result)

