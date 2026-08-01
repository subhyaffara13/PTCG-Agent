
def test_to_csv(cleared_fs, df1):
    df1.to_csv("memory://test/test.csv", index=True)

    df2 = read_csv("memory://test/test.csv", parse_dates=["dt"], index_col=0)

    expected = df1.copy()
    expected["dt"] = expected["dt"].astype("M8[us]")
    tm.assert_frame_equal(df2, expected)


def test_to_csv(data):
    # https://github.com/pandas-dev/pandas/issues/28840
    # array with list-likes fail when doing astype(str) on the numpy array
    # which was done in get_values_for_csv
    df = pd.DataFrame({"a": data})
    res = df.to_csv()
    assert str(data[0]) in res

