
def test_write_cells_merge_styled(tmp_excel):
    from pandas.io.formats.excel import ExcelCell

    sheet_name = "merge_styled"

    sty_b1 = {"font": {"color": "00FF0000"}}
    sty_a2 = {"font": {"color": "0000FF00"}}

    initial_cells = [
        ExcelCell(col=1, row=0, val=42, style=sty_b1),
        ExcelCell(col=0, row=1, val=99, style=sty_a2),
    ]

    sty_merged = {"font": {"color": "000000FF", "bold": True}}
    sty_kwargs = _OpenpyxlWriter._convert_to_style_kwargs(sty_merged)
    openpyxl_sty_merged = sty_kwargs["font"]
    merge_cells = [
        ExcelCell(
            col=0, row=0, val="pandas", mergestart=1, mergeend=1, style=sty_merged
        )
    ]

    with _OpenpyxlWriter(tmp_excel) as writer:
        writer._write_cells(initial_cells, sheet_name=sheet_name)
        writer._write_cells(merge_cells, sheet_name=sheet_name)

        wks = writer.sheets[sheet_name]
    xcell_b1 = wks["B1"]
    xcell_a2 = wks["A2"]
    assert xcell_b1.font == openpyxl_sty_merged
    assert xcell_a2.font == openpyxl_sty_merged

