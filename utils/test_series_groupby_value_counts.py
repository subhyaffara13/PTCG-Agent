
def test_series_groupby_value_counts(
    seed_nans,
    num_rows,
    max_int,
    keys,
    bins,
    isort,
    normalize,
    name,
    sort,
    ascending,
    dropna,
):
    df = seed_df(seed_nans, num_rows, max_int)

    def rebuild_index(df):
        arr = list(map(df.index.get_level_values, range(df.index.nlevels)))
        df.index = MultiIndex.from_arrays(arr, names=df.index.names)
        return df

    kwargs = {
        "normalize": normalize,
        "sort": sort,
        "ascending": ascending,
        "dropna": dropna,
        "bins": bins,
    }

    gr = df.groupby(keys, sort=isort)
    left = gr["3rd"].value_counts(**kwargs)

    gr = df.groupby(keys, sort=isort)
    right = gr["3rd"].apply(Series.value_counts, **kwargs)
    right.index.names = [*right.index.names[:-1], "3rd"]
    # https://github.com/pandas-dev/pandas/issues/49909
    right = right.rename(name)

    # have to sort on index because of unstable sort on values
    left, right = map(rebuild_index, (left, right))  # xref GH9212
    tm.assert_series_equal(left.sort_index(), right.sort_index())

