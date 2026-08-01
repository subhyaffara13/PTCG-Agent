
def test_custom_grouper_df(unit):
    index = date_range(datetime(2005, 1, 1), datetime(2005, 1, 10), freq="D")
    b = Grouper(freq=Minute(5), closed="right", label="right")
    dti = index.as_unit(unit)
    df = DataFrame(
        np.random.default_rng(2).random((len(dti), 10)), index=dti, dtype="float64"
    )
    r = df.groupby(b).agg("sum")

    assert len(r.columns) == 10
    assert len(r.index) == 2593

