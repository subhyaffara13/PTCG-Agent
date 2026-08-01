
def test_count_masked_returns_masked_dtype(dtype):
    df = DataFrame(
        {
            "A": [1, 1],
            "B": pd.array([1, pd.NA], dtype=dtype),
            "C": pd.array([1, 1], dtype=dtype),
        }
    )
    result = df.groupby("A").count()
    expected = DataFrame(
        [[1, 2]], index=Index([1], name="A"), columns=["B", "C"], dtype="Int64"
    )
    tm.assert_frame_equal(result, expected)

