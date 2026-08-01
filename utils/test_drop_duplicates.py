
def test_drop_duplicates(any_numpy_dtype, keep, expected):
    tc = Series([1, 0, 3, 5, 3, 0, 4], dtype=np.dtype(any_numpy_dtype))

    if tc.dtype == "bool":
        pytest.skip("tested separately in test_drop_duplicates_bool")

    tm.assert_series_equal(tc.duplicated(keep=keep), expected)
    tm.assert_series_equal(tc.drop_duplicates(keep=keep), tc[~expected])
    sc = tc.copy()
    return_value = sc.drop_duplicates(keep=keep, inplace=True)
    assert return_value is None
    tm.assert_series_equal(sc, tc[~expected])


def test_drop_duplicates():
    df = DataFrame(
        {
            "AAA": ["foo", "bar", "foo", "bar", "foo", "bar", "bar", "foo"],
            "B": ["one", "one", "two", "two", "two", "two", "one", "two"],
            "C": [1, 1, 2, 2, 2, 2, 1, 2],
            "D": range(8),
        }
    )
    # single column
    result = df.drop_duplicates("AAA")
    expected = df[:2]
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates("AAA", keep="last")
    expected = df.loc[[6, 7]]
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates("AAA", keep=False)
    expected = df.loc[[]]
    tm.assert_frame_equal(result, expected)
    assert len(result) == 0

    # multi column
    expected = df.loc[[0, 1, 2, 3]]
    result = df.drop_duplicates(np.array(["AAA", "B"]))
    tm.assert_frame_equal(result, expected)
    result = df.drop_duplicates(["AAA", "B"])
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates(("AAA", "B"), keep="last")
    expected = df.loc[[0, 5, 6, 7]]
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates(("AAA", "B"), keep=False)
    expected = df.loc[[0]]
    tm.assert_frame_equal(result, expected)

    # consider everything
    df2 = df.loc[:, ["AAA", "B", "C"]]

    result = df2.drop_duplicates()
    # in this case only
    expected = df2.drop_duplicates(["AAA", "B"])
    tm.assert_frame_equal(result, expected)

    result = df2.drop_duplicates(keep="last")
    expected = df2.drop_duplicates(["AAA", "B"], keep="last")
    tm.assert_frame_equal(result, expected)

    result = df2.drop_duplicates(keep=False)
    expected = df2.drop_duplicates(["AAA", "B"], keep=False)
    tm.assert_frame_equal(result, expected)

    # integers
    result = df.drop_duplicates("C")
    expected = df.iloc[[0, 2]]
    tm.assert_frame_equal(result, expected)
    result = df.drop_duplicates("C", keep="last")
    expected = df.iloc[[-2, -1]]
    tm.assert_frame_equal(result, expected)

    df["E"] = df["C"].astype("int8")
    result = df.drop_duplicates("E")
    expected = df.iloc[[0, 2]]
    tm.assert_frame_equal(result, expected)
    result = df.drop_duplicates("E", keep="last")
    expected = df.iloc[[-2, -1]]
    tm.assert_frame_equal(result, expected)

    # GH 11376
    df = DataFrame({"x": [7, 6, 3, 3, 4, 8, 0], "y": [0, 6, 5, 5, 9, 1, 2]})
    expected = df.loc[df.index != 3]
    tm.assert_frame_equal(df.drop_duplicates(), expected)

    df = DataFrame([[1, 0], [0, 2]])
    tm.assert_frame_equal(df.drop_duplicates(), df)

    df = DataFrame([[-2, 0], [0, -4]])
    tm.assert_frame_equal(df.drop_duplicates(), df)

    x = np.iinfo(np.int64).max / 3 * 2
    df = DataFrame([[-x, x], [0, x + 4]])
    tm.assert_frame_equal(df.drop_duplicates(), df)

    df = DataFrame([[-x, x], [x, x + 4]])
    tm.assert_frame_equal(df.drop_duplicates(), df)

    # GH 11864
    df = DataFrame([i] * 9 for i in range(16))
    df = concat([df, DataFrame([[1] + [0] * 8])], ignore_index=True)

    for keep in ["first", "last", False]:
        assert df.duplicated(keep=keep).sum() == 0

