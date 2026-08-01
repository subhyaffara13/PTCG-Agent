
def test_stylesheet_io(xsl_row_field_output, mode, geom_df):
    # note: By default the bodies of untyped functions are not checked,
    # consider using --check-untyped-defs
    pytest.importorskip("lxml")
    xsl_obj: BytesIO | StringIO  # type: ignore[annotation-unchecked]

    with open(
        xsl_row_field_output, mode, encoding="utf-8" if mode == "r" else None
    ) as f:
        if mode == "rb":
            xsl_obj = BytesIO(f.read())
        else:
            xsl_obj = StringIO(f.read())

    output = geom_df.to_xml(stylesheet=xsl_obj)

    assert output == xsl_expected


def test_stylesheet_io(kml_cta_rail_lines, xsl_flatten_doc, mode):
    # note: By default the bodies of untyped functions are not checked,
    # consider using --check-untyped-defs
    pytest.importorskip("lxml")
    xsl_obj: BytesIO | StringIO  # type: ignore[annotation-unchecked]

    with open(xsl_flatten_doc, mode, encoding="utf-8" if mode == "r" else None) as f:
        if mode == "rb":
            xsl_obj = BytesIO(f.read())
        else:
            xsl_obj = StringIO(f.read())

    df_style = read_xml(
        kml_cta_rail_lines,
        xpath=".//k:Placemark",
        namespaces={"k": "http://www.opengis.net/kml/2.2"},
        stylesheet=xsl_obj,
    )

    tm.assert_frame_equal(df_kml, df_style)

