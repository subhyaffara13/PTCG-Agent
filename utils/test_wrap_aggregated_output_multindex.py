
def test_wrap_aggregated_output_multindex(
    multiindex_dataframe_random_data, using_infer_string
):
    df = multiindex_dataframe_random_data.T
    df["baz", "two"] = "peekaboo"

    keys = [np.array([0, 0, 1]), np.array([0, 0, 1])]
    msg = re.escape("agg function failed [how->mean,dtype->")
    if using_infer_string:
        msg = "dtype 'str' does not support operation 'mean'"
    with pytest.raises(TypeError, match=msg):
        df.groupby(keys).agg("mean")
    agged = df.drop(columns=("baz", "two")).groupby(keys).agg("mean")
    assert isinstance(agged.columns, MultiIndex)

    def aggfun(ser):
        if ser.name == ("foo", "one"):
            raise TypeError("Test error message")
        return ser.sum()

    with pytest.raises(TypeError, match="Test error message"):
        df.groupby(keys).aggregate(aggfun)

