
def test_groupby_resample_interpolate_raises(groupy_test_df):
    # GH 35325

    # Make a copy of the test data frame that has index.name=None
    groupy_test_df_without_index_name = groupy_test_df.copy()
    groupy_test_df_without_index_name.index.name = None

    dfs = [groupy_test_df, groupy_test_df_without_index_name]

    for df in dfs:
        with pytest.raises(
            NotImplementedError,
            match="Direct interpolation of MultiIndex data frames is not supported",
        ):
            df.groupby("volume").resample("1D").interpolate(method="linear")

