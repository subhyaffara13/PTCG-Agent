
def test_map_datetimelike(col, val):
    # datetime/timedelta
    df = DataFrame(np.random.default_rng(2).random((3, 4)))
    df[col] = val
    result = df.map(str)
    assert result.loc[0, col] == str(df.loc[0, col])

