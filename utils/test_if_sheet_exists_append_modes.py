
def test_if_sheet_exists_append_modes(tmp_excel, if_sheet_exists, num_sheets, expected):
    # GH 40230
    df1 = DataFrame({"fruit": ["apple", "banana"]})
    df2 = DataFrame({"fruit": ["pear"]})

    df1.to_excel(tmp_excel, engine="openpyxl", sheet_name="foo", index=False)
    with ExcelWriter(
        tmp_excel, engine="openpyxl", mode="a", if_sheet_exists=if_sheet_exists
    ) as writer:
        df2.to_excel(writer, sheet_name="foo", index=False)

    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as wb:
        assert len(wb.sheetnames) == num_sheets
        assert wb.sheetnames[0] == "foo"
        result = pd.read_excel(wb, "foo", engine="openpyxl")
        assert list(result["fruit"]) == expected
        if len(wb.sheetnames) == 2:
            result = pd.read_excel(wb, wb.sheetnames[1], engine="openpyxl")
            tm.assert_frame_equal(result, df2)

