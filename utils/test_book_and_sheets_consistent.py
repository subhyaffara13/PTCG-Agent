
def test_book_and_sheets_consistent(tmp_excel):
    # GH#45687 - Ensure sheets is updated if user modifies book
    with ExcelWriter(tmp_excel) as writer:
        assert writer.sheets == {}
        table = odf.table.Table(name="test_name")
        writer.book.spreadsheet.addElement(table)
        assert writer.sheets == {"test_name": table}


def test_book_and_sheets_consistent(tmp_excel):
    # GH#45687 - Ensure sheets is updated if user modifies book
    with ExcelWriter(tmp_excel, engine="openpyxl") as writer:
        assert writer.sheets == {}
        sheet = writer.book.create_sheet("test_name", 0)
        assert writer.sheets == {"test_name": sheet}


def test_book_and_sheets_consistent(tmp_excel):
    # GH#45687 - Ensure sheets is updated if user modifies book
    with ExcelWriter(tmp_excel, engine="xlsxwriter") as writer:
        assert writer.sheets == {}
        sheet = writer.book.add_worksheet("test_name")
        assert writer.sheets == {"test_name": sheet}

