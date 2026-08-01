
def test_precision_zero(df):
    styler = Styler(df, precision=0)
    ctx = styler._translate(True, True)
    assert ctx["body"][0][2]["display_value"] == "-1"
    assert ctx["body"][1][2]["display_value"] == "-1"

