
def test_styler_custom_converter(tmp_excel):
    openpyxl = pytest.importorskip("openpyxl")

    def custom_converter(css):
        return {"font": {"color": {"rgb": "111222"}}}

    df = DataFrame(np.random.default_rng(2).standard_normal((1, 1)))
    styler = df.style.map(lambda x: "color: #888999")
    with ExcelWriter(tmp_excel, engine="openpyxl") as writer:
        ExcelFormatter(styler, style_converter=custom_converter).write(
            writer, sheet_name="custom"
        )

    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as wb:
        assert wb["custom"].cell(2, 2).font.color.value == "00111222"

