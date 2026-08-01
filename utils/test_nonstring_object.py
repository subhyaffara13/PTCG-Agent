
def test_nonstring_object():
    df = pd.DataFrame({"A": ["a", 10, 1.0, ()]})
    with tm.assert_produces_warning(match="Interchange"):
        col = df.__dataframe__().get_column_by_name("A")
    with pytest.raises(NotImplementedError, match="not supported yet"):
        col.dtype

