
def test_read_workbook(datapath, ext, read_only):
    # GH 39528
    filename = datapath("io", "data", "excel", "test1" + ext)
    with contextlib.closing(
        openpyxl.load_workbook(filename, read_only=read_only)
    ) as wb:
        result = pd.read_excel(wb, engine="openpyxl")
    expected = pd.read_excel(filename)
    tm.assert_frame_equal(result, expected)

