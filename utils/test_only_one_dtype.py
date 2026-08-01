
def test_only_one_dtype(test_data, df_from_dict):
    columns = list(test_data.keys())
    df = df_from_dict(test_data)
    with tm.assert_produces_warning(match="Interchange"):
        dfX = df.__dataframe__()

    column_size = len(test_data[columns[0]])
    for column in columns:
        null_count = dfX.get_column_by_name(column).null_count
        assert null_count == 0
        assert isinstance(null_count, int)
        assert dfX.get_column_by_name(column).size() == column_size
        assert dfX.get_column_by_name(column).offset == 0

