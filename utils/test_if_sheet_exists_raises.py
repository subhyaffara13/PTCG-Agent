import re

def test_if_sheet_exists_raises(tmp_excel, if_sheet_exists, msg):
    # GH 40230
    df = DataFrame({"fruit": ["pear"]})
    df.to_excel(tmp_excel, sheet_name="foo", engine="openpyxl")
    with pytest.raises(ValueError, match=re.escape(msg)):
        with ExcelWriter(
            tmp_excel, engine="openpyxl", mode="a", if_sheet_exists=if_sheet_exists
        ) as writer:
            df.to_excel(writer, sheet_name="foo")

