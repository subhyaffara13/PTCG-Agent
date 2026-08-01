
def test_ops_not_as_index(reduction_func):
    # GH 10355, 21090
    # Using as_index=False should not modify grouped column

    if reduction_func in ("corrwith", "nth", "ngroup"):
        pytest.skip(f"GH 5755: Test not applicable for {reduction_func}")

    df = DataFrame(
        np.random.default_rng(2).integers(0, 5, size=(100, 2)), columns=["a", "b"]
    )
    expected = getattr(df.groupby("a"), reduction_func)()
    if reduction_func == "size":
        expected = expected.rename("size")
    expected = expected.reset_index()

    if reduction_func != "size":
        # 32 bit compat -> groupby preserves dtype whereas reset_index casts to int64
        expected["a"] = expected["a"].astype(df["a"].dtype)

    g = df.groupby("a", as_index=False)

    result = getattr(g, reduction_func)()
    tm.assert_frame_equal(result, expected)

    result = g.agg(reduction_func)
    tm.assert_frame_equal(result, expected)

    result = getattr(g["b"], reduction_func)()
    tm.assert_frame_equal(result, expected)

    result = g["b"].agg(reduction_func)
    tm.assert_frame_equal(result, expected)

