
def test_groupby_wrong_multi_labels():
    index = Index([0, 1, 2, 3, 4], name="index")
    data = DataFrame(
        {
            "foo": ["foo1", "foo1", "foo2", "foo1", "foo3"],
            "bar": ["bar1", "bar2", "bar2", "bar1", "bar1"],
            "baz": ["baz1", "baz1", "baz1", "baz2", "baz2"],
            "spam": ["spam2", "spam3", "spam2", "spam1", "spam1"],
            "data": [20, 30, 40, 50, 60],
        },
        index=index,
    )

    grouped = data.groupby(["foo", "bar", "baz", "spam"])

    result = grouped.agg("mean")
    expected = grouped.mean()
    tm.assert_frame_equal(result, expected)

