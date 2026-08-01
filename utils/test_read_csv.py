
def test_read_csv(cleared_fs, df1):
    text = str(df1.to_csv(index=False)).encode()
    with cleared_fs.open("test/test.csv", "wb") as w:
        w.write(text)
    df2 = read_csv("memory://test/test.csv", parse_dates=["dt"])

    expected = df1.copy()
    expected["dt"] = expected["dt"].astype("M8[us]")
    tm.assert_frame_equal(df2, expected)

