from pathlib import Path


def test_append_mode_file(tmp_excel):
    # GH 39576
    df = DataFrame()

    df.to_excel(tmp_excel, engine="openpyxl")

    with ExcelWriter(
        tmp_excel, mode="a", engine="openpyxl", if_sheet_exists="new"
    ) as writer:
        df.to_excel(writer)

    # make sure that zip files are not concatenated by making sure that
    # "docProps/app.xml" only occurs twice in the file
    data = Path(tmp_excel).read_bytes()
    first = data.find(b"docProps/app.xml")
    second = data.find(b"docProps/app.xml", first + 1)
    third = data.find(b"docProps/app.xml", second + 1)
    assert second != -1 and third == -1

