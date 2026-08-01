
def test_groupby_list_level():
    # GH 9790
    expected = DataFrame(np.arange(0, 9).reshape(3, 3), dtype=float)
    result = expected.groupby(level=[0]).mean()
    tm.assert_frame_equal(result, expected)

