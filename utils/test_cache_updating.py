
def test_cache_updating():
    # 5216
    # make sure that we don't try to set a dead cache
    a = np.random.default_rng(2).random((10, 3))
    df = DataFrame(a, columns=["x", "y", "z"])
    df_original = df.copy()
    tuples = [(i, j) for i in range(5) for j in range(2)]
    index = MultiIndex.from_tuples(tuples)
    df.index = index

    # setting via chained assignment
    # but actually works, since everything is a view

    with tm.raises_chained_assignment_error():
        df.loc[0]["z"].iloc[0] = 1.0

    assert df.loc[(0, 0), "z"] == df_original.loc[0, "z"]

    # correct setting
    df.loc[(0, 0), "z"] = 2
    result = df.loc[(0, 0), "z"]
    assert result == 2

