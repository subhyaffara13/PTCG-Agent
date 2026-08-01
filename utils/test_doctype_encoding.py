
def test_doctype_encoding(styler):
    with option_context("styler.render.encoding", "ASCII"):
        result = styler.to_html(doctype_html=True)
        assert '<meta charset="ASCII">' in result
        result = styler.to_html(doctype_html=True, encoding="ANSI")
        assert '<meta charset="ANSI">' in result

