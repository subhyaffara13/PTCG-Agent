
def test_format_with_na_rep():
    # GH 21527 28358
    df = DataFrame([[None, None], [1.1, 1.2]], columns=["A", "B"])

    ctx = df.style.format(None, na_rep="-")._translate(True, True)
    assert ctx["body"][0][1]["display_value"] == "-"
    assert ctx["body"][0][2]["display_value"] == "-"

    ctx = df.style.format("{:.2%}", na_rep="-")._translate(True, True)
    assert ctx["body"][0][1]["display_value"] == "-"
    assert ctx["body"][0][2]["display_value"] == "-"
    assert ctx["body"][1][1]["display_value"] == "110.00%"
    assert ctx["body"][1][2]["display_value"] == "120.00%"

    ctx = df.style.format("{:.2%}", na_rep="-", subset=["B"])._translate(True, True)
    assert ctx["body"][0][2]["display_value"] == "-"
    assert ctx["body"][1][2]["display_value"] == "120.00%"

