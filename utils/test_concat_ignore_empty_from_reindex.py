
def test_concat_ignore_empty_from_reindex():
    # https://github.com/pandas-dev/pandas/pull/43507#issuecomment-920375856
    df1 = DataFrame({"a": [1], "b": [pd.Timestamp("2012-01-01")]})
    df2 = DataFrame({"a": [2]})

    aligned = df2.reindex(columns=df1.columns)

    result = concat([df1, aligned], ignore_index=True)

    expected = DataFrame(
        {
            "a": [1, 2],
            "b": pd.array([pd.Timestamp("2012-01-01"), np.nan], dtype=object),
        },
        dtype=object,
    )
    expected["a"] = expected["a"].astype("int64")
    tm.assert_frame_equal(result, expected)

