
def test_styler_to_excel_unstyled(engine, tmp_excel):
    # compare DataFrame.to_excel and Styler.to_excel when no styles applied
    pytest.importorskip(engine)
    df = DataFrame(np.random.default_rng(2).standard_normal((2, 2)))
    with ExcelWriter(tmp_excel, engine=engine) as writer:
        df.to_excel(writer, sheet_name="dataframe")
        df.style.to_excel(writer, sheet_name="unstyled")

    openpyxl = pytest.importorskip("openpyxl")  # test loading only with openpyxl
    with contextlib.closing(openpyxl.load_workbook(tmp_excel)) as wb:
        for col1, col2 in zip(
            wb["dataframe"].columns,
            wb["unstyled"].columns,
            strict=True,
        ):
            assert len(col1) == len(col2)
            for cell1, cell2 in zip(col1, col2, strict=True):
                assert cell1.value == cell2.value
                assert_equal_cell_styles(cell1, cell2)

