
def test_apply_to_nullable_integer_returns_float(values, function):
    # https://github.com/pandas-dev/pandas/issues/32219
    output = 0.5 if function == "var" else 1.5
    arr = np.array([output] * 3, dtype=float)
    idx = pd.Index([1, 2, 3], name="a", dtype="Int64")
    expected = DataFrame({"b": arr}, index=idx).astype("Float64")

    groups = DataFrame(values, dtype="Int64").groupby("a")

    result = getattr(groups, function)()
    tm.assert_frame_equal(result, expected)

    result = groups.agg(function)
    tm.assert_frame_equal(result, expected)

    result = groups.agg([function])
    expected.columns = MultiIndex.from_tuples([("b", function)])
    tm.assert_frame_equal(result, expected)

