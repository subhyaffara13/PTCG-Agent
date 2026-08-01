
def test_series_grouper_noncontig_index():
    index = Index(["a" * 10] * 100)

    values = Series(np.random.default_rng(2).standard_normal(50), index=index[::2])
    labels = np.random.default_rng(2).integers(0, 5, 50)

    # it works!
    grouped = values.groupby(labels)

    # accessing the index elements causes segfault
    f = lambda x: len(set(map(id, x.index)))
    grouped.agg(f)

