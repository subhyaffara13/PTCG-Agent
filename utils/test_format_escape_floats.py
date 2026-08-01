
def test_format_escape_floats(styler):
    # test given formatter for number format is not impacted by escape
    s = styler.format("{:.1f}", escape="html")
    for expected in [">0.0<", ">1.0<", ">-1.2<", ">-0.6<"]:
        assert expected in s.to_html()
    # tests precision of floats is not impacted by escape
    s = styler.format(precision=1, escape="html")
    for expected in [">0<", ">1<", ">-1.2<", ">-0.6<"]:
        assert expected in s.to_html()

