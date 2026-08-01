
def test_isin_generator():
    # GH#52568
    midx = MultiIndex.from_tuples([(1, 2)])
    result = midx.isin(x for x in [(1, 2)])
    expected = np.array([True])
    tm.assert_numpy_array_equal(result, expected)

