
def test_read_xlrd_book(read_ext_xlrd, datapath):
    engine = "xlrd"
    sheet_name = "Sheet1"
    pth = datapath("io", "data", "excel", "test1.xls")
    with xlrd.open_workbook(pth) as book:
        with ExcelFile(book, engine=engine) as xl:
            result = pd.read_excel(xl, sheet_name=sheet_name, index_col=0)

        expected = pd.read_excel(
            book, sheet_name=sheet_name, engine=engine, index_col=0
        )
    tm.assert_frame_equal(result, expected)

