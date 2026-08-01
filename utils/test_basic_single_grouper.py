
def test_basic_single_grouper():
    cat1 = Categorical(["a", "a", "b", "b"], categories=["a", "b", "z"], ordered=True)
    cat2 = Categorical(["c", "d", "c", "d"], categories=["c", "d", "y"], ordered=True)
    df = DataFrame({"A": cat1, "B": cat2, "values": [1, 2, 3, 4]})

    gb = df.groupby("A", observed=False)
    exp_idx = CategoricalIndex(["a", "b", "z"], name="A", ordered=True)
    expected = DataFrame({"values": Series([3, 7, 0], index=exp_idx)})
    result = gb.sum(numeric_only=True)
    tm.assert_frame_equal(result, expected)

