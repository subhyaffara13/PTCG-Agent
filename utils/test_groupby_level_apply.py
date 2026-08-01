
def test_groupby_level_apply(multiindex_dataframe_random_data):
    result = multiindex_dataframe_random_data.groupby(level=0).count()
    assert result.index.name == "first"
    result = multiindex_dataframe_random_data.groupby(level=1).count()
    assert result.index.name == "second"

    result = multiindex_dataframe_random_data["A"].groupby(level=0).count()
    assert result.index.name == "first"

