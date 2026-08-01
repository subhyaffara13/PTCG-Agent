
def test_engine_kwargs_append_data_only(tmp_excel, data_only, expected):
    # GH 43445
    # tests whether the data_only engine_kwarg actually works well for
    # openpyxl's load_workbook
    DataFrame(["=1+1"]).to_excel(tmp_excel)
    with ExcelWriter(
        tmp_excel, engine="openpyxl", mode="a", engine_kwargs={"data_only": data_only}
    ) as writer:
        assert writer.sheets["Sheet1"]["B2"].value == expected
        # ExcelWriter needs us to writer something to close properly?
        DataFrame().to_excel(writer, sheet_name="Sheet2")

    # ensure that data_only also works for reading
    #  and that formulas/values roundtrip
    assert (
        pd.read_excel(
            tmp_excel,
            sheet_name="Sheet1",
            engine="openpyxl",
            engine_kwargs={"data_only": data_only},
        ).iloc[0, 1]
        == expected
    )

