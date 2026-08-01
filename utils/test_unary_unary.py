
def test_unary_unary(dtype):
    # unary input, unary output
    values = np.array([[-1, -1], [1, 1]], dtype="int64")
    df = pd.DataFrame(values, columns=["A", "B"], index=["a", "b"]).astype(dtype=dtype)
    result = np.positive(df)
    expected = pd.DataFrame(
        np.positive(values), index=df.index, columns=df.columns
    ).astype(dtype)
    tm.assert_frame_equal(result, expected)

