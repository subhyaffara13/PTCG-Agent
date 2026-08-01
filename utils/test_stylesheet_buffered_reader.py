
def test_stylesheet_buffered_reader(xsl_row_field_output, mode, geom_df):
    pytest.importorskip("lxml")
    with open(
        xsl_row_field_output, mode, encoding="utf-8" if mode == "r" else None
    ) as f:
        output = geom_df.to_xml(stylesheet=f)

    assert output == xsl_expected


def test_stylesheet_buffered_reader(kml_cta_rail_lines, xsl_flatten_doc, mode):
    pytest.importorskip("lxml")
    with open(xsl_flatten_doc, mode, encoding="utf-8" if mode == "r" else None) as f:
        df_style = read_xml(
            kml_cta_rail_lines,
            xpath=".//k:Placemark",
            namespaces={"k": "http://www.opengis.net/kml/2.2"},
            stylesheet=f,
        )

    tm.assert_frame_equal(df_kml, df_style)

