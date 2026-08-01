
def test_apply_empty_string_nan_coerce_bug():
    # GH#24903
    result = (
        DataFrame(
            {
                "a": [1, 1, 2, 2],
                "b": ["", "", "", ""],
                "c": pd.to_datetime([1, 2, 3, 4], unit="s"),
            }
        )
        .groupby(["a", "b"])
        .apply(lambda df: df.iloc[-1])
    )
    expected = DataFrame(
        [[pd.to_datetime(2, unit="s")], [pd.to_datetime(4, unit="s")]],
        columns=["c"],
        index=MultiIndex.from_tuples([(1, ""), (2, "")], names=["a", "b"]),
    )
    tm.assert_frame_equal(result, expected)

