
def test_read_old_xls_files(file_header):
    # GH 41226
    f = io.BytesIO(file_header)
    assert inspect_excel_format(f) == "xls"

