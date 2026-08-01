
def test_apply_with_mixed_dtype():
    # GH3480, apply with mixed dtype on axis=1 breaks in 0.11
    df = DataFrame(
        {
            "foo1": np.random.default_rng(2).standard_normal(6),
            "foo2": ["one", "two", "two", "three", "one", "two"],
        }
    )
    result = df.apply(lambda x: x, axis=1)
    expected = df
    tm.assert_frame_equal(result, expected)

    # GH 3610 incorrect dtype conversion with as_index=False
    df = DataFrame({"c1": [1, 2, 6, 6, 8]})
    df["c2"] = df.c1 / 2.0
    result1 = df.groupby("c2").mean().reset_index()
    result2 = df.groupby("c2", as_index=False).mean()
    tm.assert_frame_equal(result1, result2)

