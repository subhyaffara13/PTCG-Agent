
def test_display_format_index(styler, index, columns):
    exp_index = ["x", "y"]
    if index:
        styler.format_index(lambda v: v.upper(), axis=0)  # test callable
        exp_index = ["X", "Y"]

    exp_columns = ["A", "B"]
    if columns:
        styler.format_index("*{}*", axis=1)  # test string
        exp_columns = ["*A*", "*B*"]

    ctx = styler._translate(True, True)

    for r, row in enumerate(ctx["body"]):
        assert row[0]["display_value"] == exp_index[r]

    for c, col in enumerate(ctx["head"][1:]):
        assert col["display_value"] == exp_columns[c]

