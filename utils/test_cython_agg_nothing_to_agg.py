
def test_cython_agg_nothing_to_agg():
    frame = DataFrame(
        {"a": np.random.default_rng(2).integers(0, 5, 50), "b": ["foo", "bar"] * 25}
    )

    msg = "Cannot use numeric_only=True with SeriesGroupBy.mean and non-numeric dtypes"
    with pytest.raises(TypeError, match=msg):
        frame.groupby("a")["b"].mean(numeric_only=True)

    frame = DataFrame(
        {"a": np.random.default_rng(2).integers(0, 5, 50), "b": ["foo", "bar"] * 25}
    )

    result = frame[["b"]].groupby(frame["a"]).mean(numeric_only=True)
    expected = DataFrame(
        [],
        index=frame["a"].sort_values().drop_duplicates(),
        columns=Index([], dtype="str"),
    )
    tm.assert_frame_equal(result, expected)

