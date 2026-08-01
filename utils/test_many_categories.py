
def test_many_categories(as_index, sort, index_kind, ordered):
    # GH#48749 - Test when the grouper has many categories
    if index_kind != "range" and not as_index:
        pytest.skip(reason="Result doesn't have categories, nothing to test")
    categories = np.arange(9999, -1, -1)
    grouper = Categorical([2, 1, 2, 3], categories=categories, ordered=ordered)
    df = DataFrame({"a": grouper, "b": range(4)})
    if index_kind == "range":
        keys = ["a"]
    elif index_kind == "single":
        keys = ["a"]
        df = df.set_index(keys)
    elif index_kind == "multi":
        keys = ["a", "a2"]
        df["a2"] = df["a"]
        df = df.set_index(keys)
    gb = df.groupby(keys, as_index=as_index, sort=sort, observed=True)
    result = gb.sum()

    # Test is setup so that data and index are the same values
    data = [3, 2, 1] if sort else [2, 1, 3]

    index = CategoricalIndex(
        data, categories=grouper.categories, ordered=ordered, name="a"
    )
    if as_index:
        expected = DataFrame({"b": data})
        if index_kind == "multi":
            expected.index = MultiIndex.from_frame(DataFrame({"a": index, "a2": index}))
        else:
            expected.index = index
    elif index_kind == "multi":
        expected = DataFrame({"a": Series(index), "a2": Series(index), "b": data})
    else:
        expected = DataFrame({"a": Series(index), "b": data})

    tm.assert_frame_equal(result, expected)

