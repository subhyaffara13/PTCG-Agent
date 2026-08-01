
def test_handle_dict_return_value(df):
    def f(group):
        return {"max": group.max(), "min": group.min()}

    def g(group):
        return Series({"max": group.max(), "min": group.min()})

    result = df.groupby("A")["C"].apply(f)
    expected = df.groupby("A")["C"].apply(g)

    assert isinstance(result, Series)
    tm.assert_series_equal(result, expected)

