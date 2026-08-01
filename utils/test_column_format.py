
def test_column_format(tmp_excel):
    # Test that column formats are applied to cells. Test for issue #9167.
    # Applicable to xlsxwriter only.
    openpyxl = pytest.importorskip("openpyxl")

    frame = DataFrame({"A": [123456, 123456], "B": [123456, 123456]})

    with ExcelWriter(tmp_excel) as writer:
        frame.to_excel(writer)

        # Add a number format to col B and ensure it is applied to cells.
        num_format = "#,##0"
        write_workbook = writer.book
        write_worksheet = write_workbook.worksheets()[0]
        col_format = write_workbook.add_format({"num_format": num_format})
        write_worksheet.set_column("B:B", None, col_format)

    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as read_workbook:
        try:
            read_worksheet = read_workbook["Sheet1"]
        except TypeError:
            # compat
            read_worksheet = read_workbook.get_sheet_by_name(name="Sheet1")

    # Get the number format from the cell.
    try:
        cell = read_worksheet["B2"]
    except TypeError:
        # compat
        cell = read_worksheet.cell("B2")

    try:
        read_num_format = cell.number_format
    except AttributeError:
        read_num_format = cell.style.number_format._format_code

    assert read_num_format == num_format


def test_column_format(styler):
    # default setting is already tested in `test_latex_minimal_tabular`
    styler.set_table_styles([{"selector": "column_format", "props": ":cccc"}])

    assert "\\begin{tabular}{rrrr}" in styler.to_latex(column_format="rrrr")
    styler.set_table_styles([{"selector": "column_format", "props": ":r|r|cc"}])
    assert "\\begin{tabular}{r|r|cc}" in styler.to_latex()

