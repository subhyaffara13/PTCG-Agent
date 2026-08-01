
def test_format_with_precision(precision, expected):
    # Issue #13257
    df = DataFrame([[1.0, 2.0090, 3.2121, 4.566]], columns=[1.0, 2.0090, 3.2121, 4.566])
    styler = Styler(df)
    styler.format(precision=precision)
    styler.format_index(precision=precision, axis=1)

    ctx = styler._translate(True, True)
    for col, exp in enumerate(expected):
        assert ctx["body"][0][col + 1]["display_value"] == exp  # format test
        assert ctx["head"][0][col + 1]["display_value"] == exp  # format_index test

