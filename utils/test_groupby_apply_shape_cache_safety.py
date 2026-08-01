
def test_groupby_apply_shape_cache_safety():
    # GH#42702 this fails if we cache_readonly Block.shape
    df = DataFrame({"A": ["a", "a", "b"], "B": [1, 2, 3], "C": [4, 6, 5]})
    gb = df.groupby("A")
    result = gb[["B", "C"]].apply(lambda x: x.astype(float).max() - x.min())

    expected = DataFrame(
        {"B": [1.0, 0.0], "C": [2.0, 0.0]}, index=Index(["a", "b"], name="A")
    )
    tm.assert_frame_equal(result, expected)

