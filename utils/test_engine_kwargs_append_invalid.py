import re

def test_engine_kwargs_append_invalid(tmp_excel):
    # GH 43445
    # test whether an invalid engine kwargs actually raises
    DataFrame(["hello", "world"]).to_excel(tmp_excel)
    with pytest.raises(
        TypeError,
        match=re.escape(
            "load_workbook() got an unexpected keyword argument 'apple_banana'"
        ),
    ):
        with ExcelWriter(
            tmp_excel,
            engine="openpyxl",
            mode="a",
            engine_kwargs={"apple_banana": "fruit"},
        ) as writer:
            # ExcelWriter needs us to write something to close properly
            DataFrame(["good"]).to_excel(writer, sheet_name="Sheet2")

