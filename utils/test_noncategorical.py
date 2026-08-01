
def test_noncategorical(df_from_dict):
    df = df_from_dict({"a": [1, 2, 3]})
    with tm.assert_produces_warning(match="Interchange"):
        dfX = df.__dataframe__()
    colX = dfX.get_column_by_name("a")
    with pytest.raises(TypeError, match=".*categorical.*"):
        colX.describe_categorical

