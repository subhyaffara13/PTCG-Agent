
def test_add_frame(dtype):
    arr = pd.array(["a", "b", np.nan, np.nan], dtype=dtype)
    df = pd.DataFrame([["x", np.nan, "y", np.nan]])

    assert arr.__add__(df) is NotImplemented

    result = arr + df
    expected = pd.DataFrame([["ax", np.nan, np.nan, np.nan]]).astype(dtype)
    tm.assert_frame_equal(result, expected)

    result = df + arr
    expected = pd.DataFrame([["xa", np.nan, np.nan, np.nan]]).astype(dtype)
    tm.assert_frame_equal(result, expected)

