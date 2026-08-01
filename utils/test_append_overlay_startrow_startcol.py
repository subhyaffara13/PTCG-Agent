
def test_append_overlay_startrow_startcol(
    tmp_excel, startrow, startcol, greeting, goodbye
):
    df1 = DataFrame({"greeting": ["hello", "world"], "goodbye": ["goodbye", "people"]})
    df2 = DataFrame(["poop"])

    df1.to_excel(tmp_excel, engine="openpyxl", sheet_name="poo", index=False)
    with ExcelWriter(
        tmp_excel, engine="openpyxl", mode="a", if_sheet_exists="overlay"
    ) as writer:
        # use startrow+1 because we don't have a header
        df2.to_excel(
            writer,
            index=False,
            header=False,
            startrow=startrow + 1,
            startcol=startcol,
            sheet_name="poo",
        )

    result = pd.read_excel(tmp_excel, sheet_name="poo", engine="openpyxl")
    expected = DataFrame({"greeting": greeting, "goodbye": goodbye})
    tm.assert_frame_equal(result, expected)

