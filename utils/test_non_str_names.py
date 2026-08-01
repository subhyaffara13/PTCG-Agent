
def test_non_str_names():
    # https://github.com/pandas-dev/pandas/issues/56701
    df = pd.Series([1, 2, 3], name=0).to_frame()
    with tm.assert_produces_warning(match="Interchange"):
        names = df.__dataframe__().column_names()
    assert names == ["0"]

