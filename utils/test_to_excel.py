
def test_to_excel(cleared_fs, df1):
    pytest.importorskip("openpyxl")
    ext = "xlsx"
    path = f"memory://test/test.{ext}"
    df1.to_excel(path, index=True)

    df2 = read_excel(path, parse_dates=["dt"], index_col=0)

    expected = df1.copy()
    expected["dt"] = expected["dt"].astype("M8[us]")
    tm.assert_frame_equal(df2, expected)

