
def test_transform_transformation_func(transformation_func):
    # GH 30918
    df = DataFrame(
        {
            "A": ["foo", "foo", "foo", "foo", "bar", "bar", "baz"],
            "B": [1, 2, np.nan, 3, 3, np.nan, 4],
        },
        index=date_range("2020-01-01", "2020-01-07"),
    )
    if transformation_func == "cumcount":
        test_op = lambda x: x.transform("cumcount")
        mock_op = lambda x: Series(range(len(x)), x.index)
    elif transformation_func == "ngroup":
        test_op = lambda x: x.transform("ngroup")
        counter = -1

        def mock_op(x):
            nonlocal counter
            counter += 1
            return Series(counter, index=x.index)

    else:
        test_op = lambda x: x.transform(transformation_func)
        mock_op = lambda x: getattr(x, transformation_func)()

    result = test_op(df.groupby("A"))

    # pass the group in same order as iterating `for ... in df.groupby(...)`
    # but reorder to match df's index since this is a transform
    groups = [df[["B"]].iloc[4:6], df[["B"]].iloc[6:], df[["B"]].iloc[:4]]
    expected = concat([mock_op(g) for g in groups]).sort_index()
    # sort_index does not preserve the freq
    expected = expected.set_axis(df.index)

    if transformation_func in ("cumcount", "ngroup"):
        tm.assert_series_equal(result, expected)
    else:
        tm.assert_frame_equal(result, expected)

