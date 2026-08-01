
def test_assert_frame_equal_ts_column():
    # GH#50323
    df1 = DataFrame({"a": [pd.Timestamp("2019-12-31"), pd.Timestamp("2020-12-31")]})
    df2 = DataFrame({"a": [pd.Timestamp("2020-12-31"), pd.Timestamp("2020-12-31")]})

    msg = r'DataFrame.iloc\[:, 0\] \(column name="a"\) values are different'
    with pytest.raises(AssertionError, match=msg):
        tm.assert_frame_equal(df1, df2)

