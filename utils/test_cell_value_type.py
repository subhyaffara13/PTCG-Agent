
def test_cell_value_type(
    tmp_excel, value, cell_value_type, cell_value_attribute, cell_value
):
    # GH#54994 ODS: cell attributes should follow specification
    # http://docs.oasis-open.org/office/v1.2/os/OpenDocument-v1.2-os-part1.html#refTable13
    from odf.namespaces import OFFICENS
    from odf.table import (
        TableCell,
        TableRow,
    )

    table_cell_name = TableCell().qname

    pd.DataFrame([[value]]).to_excel(tmp_excel, header=False, index=False)

    with pd.ExcelFile(tmp_excel) as wb:
        sheet = wb._reader.get_sheet_by_index(0)
        sheet_rows = sheet.getElementsByType(TableRow)
        sheet_cells = [
            x
            for x in sheet_rows[0].childNodes
            if hasattr(x, "qname") and x.qname == table_cell_name
        ]

        cell = sheet_cells[0]
        assert cell.attributes.get((OFFICENS, "value-type")) == cell_value_type
        assert cell.attributes.get((OFFICENS, cell_value_attribute)) == cell_value

