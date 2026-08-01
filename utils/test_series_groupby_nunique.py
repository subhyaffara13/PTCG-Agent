
def test_series_groupby_nunique(sort, dropna, as_index, with_nan, keys):
    n = 100
    m = 10
    days = date_range("2015-08-23", periods=10)
    df = DataFrame(
        {
            "jim": np.random.default_rng(2).choice(list(ascii_lowercase), n),
            "joe": np.random.default_rng(2).choice(days, n),
            "julie": np.random.default_rng(2).integers(0, m, n),
        }
    )
    if with_nan:
        df = df.astype({"julie": float})  # Explicit cast to avoid implicit cast below
        df.loc[1::17, "jim"] = None
        df.loc[3::37, "joe"] = None
        df.loc[7::19, "julie"] = None
        df.loc[8::19, "julie"] = None
        df.loc[9::19, "julie"] = None
    original_df = df.copy()
    gr = df.groupby(keys, as_index=as_index, sort=sort)
    left = gr["julie"].nunique(dropna=dropna)

    gr = df.groupby(keys, as_index=as_index, sort=sort)
    right = gr["julie"].apply(Series.nunique, dropna=dropna)
    if not as_index:
        right = right.reset_index(drop=True)

    if as_index:
        tm.assert_series_equal(left, right, check_names=False)
    else:
        tm.assert_frame_equal(left, right, check_names=False)
    tm.assert_frame_equal(df, original_df)

