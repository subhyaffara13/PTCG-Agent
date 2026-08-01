
def test_stylesheet_file(kml_cta_rail_lines, xsl_flatten_doc):
    pytest.importorskip("lxml")
    df_style = read_xml(
        kml_cta_rail_lines,
        xpath=".//k:Placemark",
        namespaces={"k": "http://www.opengis.net/kml/2.2"},
        stylesheet=xsl_flatten_doc,
    )

    df_iter = read_xml(
        kml_cta_rail_lines,
        iterparse={
            "Placemark": [
                "id",
                "name",
                "styleUrl",
                "extrude",
                "altitudeMode",
                "coordinates",
            ]
        },
    )

    tm.assert_frame_equal(df_kml, df_style)
    tm.assert_frame_equal(df_kml, df_iter)

