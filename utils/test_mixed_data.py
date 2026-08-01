
def test_mixed_data(data):
    df = pd.DataFrame(data)
    with tm.assert_produces_warning(match="Interchange"):
        df2 = df.__dataframe__()

    for col_name in df.columns:
        assert df2.get_column_by_name(col_name).null_count == 0

