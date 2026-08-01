
def test_empty_string_column():
    # https://github.com/pandas-dev/pandas/issues/56703
    df = pd.DataFrame({"a": []}, dtype=str)
    with tm.assert_produces_warning(match="Interchange"):
        df2 = df.__dataframe__()
        result = pd.api.interchange.from_dataframe(df2)
    tm.assert_frame_equal(df, result)

