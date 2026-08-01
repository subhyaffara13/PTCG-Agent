
def test_pow_with_realignment():
    # GH#32685 pow has special semantics for operating with null values
    left = DataFrame({"A": [0, 1, 2]})
    right = DataFrame(index=[0, 1, 2])

    result = left**right
    expected = DataFrame({"A": [np.nan, 1.0, np.nan]})
    tm.assert_frame_equal(result, expected)

