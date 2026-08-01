
def test_loc_get_scalar_casting_to_float():
    # GH#41369
    df = DataFrame(
        {"a": 1.0, "b": 2}, index=MultiIndex.from_arrays([[3], [4]], names=["c", "d"])
    )
    result = df.loc[(3, 4), "b"]
    assert result == 2
    assert isinstance(result, np.int64)
    result = df.loc[[(3, 4)], "b"].iloc[0]
    assert result == 2
    assert isinstance(result, np.int64)

