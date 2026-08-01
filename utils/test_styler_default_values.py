
def test_styler_default_values(tmp_excel):
    # GH 54154
    openpyxl = pytest.importorskip("openpyxl")
    df = DataFrame([{"A": 1, "B": 2, "C": 3}, {"A": 1, "B": 2, "C": 3}])

    with ExcelWriter(tmp_excel, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="custom")

    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as wb:
        # Check font, spacing, indentation
        assert wb["custom"].cell(1, 1).font.bold is False
        assert wb["custom"].cell(1, 1).alignment.horizontal is None
        assert wb["custom"].cell(1, 1).alignment.vertical is None

        # Check border
        assert wb["custom"].cell(1, 1).border.bottom.color is None
        assert wb["custom"].cell(1, 1).border.top.color is None
        assert wb["custom"].cell(1, 1).border.left.color is None
        assert wb["custom"].cell(1, 1).border.right.color is None

