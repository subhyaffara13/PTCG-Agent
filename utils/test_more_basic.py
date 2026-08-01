
def test_more_basic():
    levels = ["foo", "bar", "baz", "qux"]
    codes = np.random.default_rng(2).integers(0, 4, size=10)

    cats = Categorical.from_codes(codes, levels, ordered=True)

    data = DataFrame(np.random.default_rng(2).standard_normal((10, 4)))

    result = data.groupby(cats, observed=False).mean()

    expected = data.groupby(np.asarray(cats), observed=False).mean()
    exp_idx = CategoricalIndex(levels, categories=cats.categories, ordered=True)
    expected = expected.reindex(exp_idx)

    tm.assert_frame_equal(result, expected)

    grouped = data.groupby(cats, observed=False)
    desc_result = grouped.describe()

    idx = cats.codes.argsort()
    ord_labels = np.asarray(cats).take(idx)
    ord_data = data.take(idx)

    exp_cats = Categorical(
        ord_labels, ordered=True, categories=["foo", "bar", "baz", "qux"]
    )
    expected = ord_data.groupby(exp_cats, sort=False, observed=False).describe()
    tm.assert_frame_equal(desc_result, expected)

    # GH 10460
    expc = Categorical.from_codes(np.arange(4).repeat(8), levels, ordered=True)
    exp = CategoricalIndex(expc)
    tm.assert_index_equal(desc_result.stack().index.get_level_values(0), exp)
    exp = Index(["count", "mean", "std", "min", "25%", "50%", "75%", "max"] * 4)
    tm.assert_index_equal(desc_result.stack().index.get_level_values(1), exp)

