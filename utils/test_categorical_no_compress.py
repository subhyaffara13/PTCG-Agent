
def test_categorical_no_compress():
    data = Series(np.random.default_rng(2).standard_normal(9))

    codes = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
    cats = Categorical.from_codes(codes, [0, 1, 2], ordered=True)

    result = data.groupby(cats, observed=False).mean()
    exp = data.groupby(codes, observed=False).mean()

    exp.index = CategoricalIndex(
        exp.index, categories=cats.categories, ordered=cats.ordered
    )
    tm.assert_series_equal(result, exp)

    codes = np.array([0, 0, 0, 1, 1, 1, 3, 3, 3])
    cats = Categorical.from_codes(codes, [0, 1, 2, 3], ordered=True)

    result = data.groupby(cats, observed=False).mean()
    exp = data.groupby(codes, observed=False).mean().reindex(cats.categories)
    exp.index = CategoricalIndex(
        exp.index, categories=cats.categories, ordered=cats.ordered
    )
    tm.assert_series_equal(result, exp)

