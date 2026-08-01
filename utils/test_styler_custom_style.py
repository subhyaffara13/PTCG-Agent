
def test_styler_custom_style(tmp_excel):
    # GH 54154
    css_style = "background-color: #111222"
    openpyxl = pytest.importorskip("openpyxl")
    df = DataFrame([{"A": 1, "B": 2}, {"A": 1, "B": 2}])

    with ExcelWriter(tmp_excel, engine="openpyxl") as writer:
        styler = df.style.map(lambda x: css_style)
        styler.to_excel(writer, sheet_name="custom", index=False)

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

        # Check background color
        assert wb["custom"].cell(2, 1).fill.fgColor.index == "00111222"
        assert wb["custom"].cell(3, 1).fill.fgColor.index == "00111222"
        assert wb["custom"].cell(2, 2).fill.fgColor.index == "00111222"
        assert wb["custom"].cell(3, 2).fill.fgColor.index == "00111222"

