
def test_resample_nunique_preserves_column_level_names(unit):
    # see gh-23222
    df = DataFrame(
        np.random.default_rng(2).standard_normal((5, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=5, freq="D"),
    ).abs()
    df.index = df.index.as_unit(unit)
    df.columns = pd.MultiIndex.from_arrays(
        [df.columns.tolist()] * 2, names=["lev0", "lev1"]
    )
    result = df.resample("1h").nunique()
    tm.assert_index_equal(df.columns, result.columns)

