
def test_dataframe_raises():
    # GH#51167 don't accidentally cast to StringArray by doing inference on columns
    df = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
    msg = "Cannot pass DataFrame to 'pandas.array'"
    with pytest.raises(TypeError, match=msg):
        pd.array(df)

