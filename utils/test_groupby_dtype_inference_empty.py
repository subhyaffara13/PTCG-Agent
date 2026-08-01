
def test_groupby_dtype_inference_empty():
    # GH 6733
    df = DataFrame({"x": [], "range": np.arange(0, dtype="int64")})
    assert df["x"].dtype == np.float64

    result = df.groupby("x").first()
    exp_index = Index([], name="x", dtype=np.float64)
    expected = DataFrame({"range": Series([], index=exp_index, dtype="int64")})
    tm.assert_frame_equal(result, expected, by_blocks=True)

