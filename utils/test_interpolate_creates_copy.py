
def test_interpolate_creates_copy():
    # GH#51126
    df = DataFrame({"a": [1.5, np.nan, 3]})
    view = df[:]
    expected = df.copy()

    df.ffill(inplace=True)
    df.iloc[0, 0] = 100.5
    tm.assert_frame_equal(view, expected)

