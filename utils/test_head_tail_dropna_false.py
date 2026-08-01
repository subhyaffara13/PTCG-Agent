
def test_head_tail_dropna_false():
    # GH#45089
    df = DataFrame([["a", "z"], ["b", np.nan], ["c", np.nan]], columns=["X", "Y"])
    expected = DataFrame([["a", "z"], ["b", np.nan], ["c", np.nan]], columns=["X", "Y"])

    result = df.groupby(["X", "Y"], dropna=False).head(n=1)
    tm.assert_frame_equal(result, expected)

    result = df.groupby(["X", "Y"], dropna=False).tail(n=1)
    tm.assert_frame_equal(result, expected)

    result = df.groupby(["X", "Y"], dropna=False).nth(n=0)
    tm.assert_frame_equal(result, expected)

