
def test_stylesheet_file_close(kml_cta_rail_lines, xsl_flatten_doc, mode):
    # note: By default the bodies of untyped functions are not checked,
    # consider using --check-untyped-defs
    pytest.importorskip("lxml")
    xsl_obj: BytesIO | StringIO  # type: ignore[annotation-unchecked]

    with open(xsl_flatten_doc, mode, encoding="utf-8" if mode == "r" else None) as f:
        if mode == "rb":
            xsl_obj = BytesIO(f.read())
        else:
            xsl_obj = StringIO(f.read())

        read_xml(kml_cta_rail_lines, stylesheet=xsl_obj)

        assert not f.closed

