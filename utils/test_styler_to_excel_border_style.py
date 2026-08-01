
def test_styler_to_excel_border_style(engine, border_style, tmp_excel):
    css = f"border-left: {border_style} black thin"
    attrs = ["border", "left", "style"]
    expected = border_style

    pytest.importorskip(engine)
    df = DataFrame(np.random.default_rng(2).standard_normal((1, 1)))
    styler = df.style.map(lambda x: css)

    with ExcelWriter(tmp_excel, engine=engine) as writer:
        df.to_excel(writer, sheet_name="dataframe")
        styler.to_excel(writer, sheet_name="styled")

    openpyxl = pytest.importorskip("openpyxl")  # test loading only with openpyxl
    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as wb:
        # test unstyled data cell does not have expected styles
        # test styled cell has expected styles
        u_cell, s_cell = wb["dataframe"].cell(2, 2), wb["styled"].cell(2, 2)
    for attr in attrs:
        u_cell, s_cell = getattr(u_cell, attr, None), getattr(s_cell, attr)

    if isinstance(expected, dict):
        assert u_cell is None or u_cell != expected[engine]
        assert s_cell == expected[engine]
    else:
        assert u_cell is None or u_cell != expected
        assert s_cell == expected

