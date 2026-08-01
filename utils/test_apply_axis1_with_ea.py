
def test_apply_axis1_with_ea():
    # GH#36785
    expected = DataFrame({"A": [Timestamp("2013-01-01", tz="UTC")]})
    result = expected.apply(lambda x: x, axis=1)
    tm.assert_frame_equal(result, expected)

