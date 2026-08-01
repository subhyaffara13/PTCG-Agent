
def test_write_append_mode(tmp_excel, mode, expected):
    df = DataFrame([1], columns=["baz"])

    wb = openpyxl.Workbook()
    wb.worksheets[0].title = "foo"
    wb.worksheets[0]["A1"].value = "foo"
    wb.create_sheet("bar")
    wb.worksheets[1]["A1"].value = "bar"
    wb.save(tmp_excel)

    with ExcelWriter(tmp_excel, engine="openpyxl", mode=mode) as writer:
        df.to_excel(writer, sheet_name="baz", index=False)

    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as wb2:
        result = [sheet.title for sheet in wb2.worksheets]
        assert result == expected

        for index, cell_value in enumerate(expected):
            assert wb2.worksheets[index]["A1"].value == cell_value

