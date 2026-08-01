
def test_read_empty_with_blank_row(datapath, ext, read_only):
    # GH 39547 - empty excel file with a row that has no data
    path = datapath("io", "data", "excel", f"empty_with_blank_row{ext}")
    if read_only is None:
        result = pd.read_excel(path)
    else:
        with contextlib.closing(
            openpyxl.load_workbook(path, read_only=read_only)
        ) as wb:
            result = pd.read_excel(wb, engine="openpyxl")
    expected = DataFrame()
    tm.assert_frame_equal(result, expected)

