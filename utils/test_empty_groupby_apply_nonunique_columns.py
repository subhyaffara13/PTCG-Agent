
def test_empty_groupby_apply_nonunique_columns():
    # GH#44417
    df = DataFrame(np.random.default_rng(2).standard_normal((0, 4)))
    df[3] = df[3].astype(np.int64)
    df.columns = [0, 1, 2, 0]
    gb = df.groupby(df[1], group_keys=False)
    res = gb.apply(lambda x: x)
    assert (res.dtypes == df.drop(columns=1).dtypes).all()

