
def test_get_nonexistent_category():
    # Accessing a Category that is not in the dataframe
    df = DataFrame({"var": ["a", "a", "b", "b"], "val": range(4)})
    with pytest.raises(KeyError, match="'vau'"):
        df.groupby("var").apply(lambda rows: DataFrame({"val": [rows.iloc[-1]["vau"]]}))

