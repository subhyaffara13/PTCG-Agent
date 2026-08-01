
def test_filter_against_workaround_floats():
    # Series of floats
    s = 100 * Series(np.random.default_rng(2).random(10))
    grouper = s.apply(lambda x: np.round(x, -1))
    grouped = s.groupby(grouper)
    f = lambda x: x.mean() > 10
    old_way = s[grouped.transform(f).astype("bool")]
    new_way = grouped.filter(f)
    tm.assert_series_equal(new_way.sort_values(), old_way.sort_values())

