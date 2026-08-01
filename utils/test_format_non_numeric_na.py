
def test_format_non_numeric_na():
    # GH 21527 28358
    df = DataFrame(
        {
            "object": [None, np.nan, "foo"],
            "datetime": [None, NaT, Timestamp("20120101")],
        }
    )
    ctx = df.style.format(None, na_rep="-")._translate(True, True)
    assert ctx["body"][0][1]["display_value"] == "-"
    assert ctx["body"][0][2]["display_value"] == "-"
    assert ctx["body"][1][1]["display_value"] == "-"
    assert ctx["body"][1][2]["display_value"] == "-"

