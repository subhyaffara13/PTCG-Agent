
def test_prefix_namespace(parser, temp_file):
    df_nmsp = read_xml(
        StringIO(xml_prefix_nmsp),
        xpath=".//doc:row",
        namespaces={"doc": "http://example.com"},
        parser=parser,
    )
    df_iter = read_xml_iterparse(
        xml_prefix_nmsp,
        temp_file,
        parser=parser,
        iterparse={"row": ["shape", "degrees", "sides"]},
    )

    df_expected = DataFrame(
        {
            "shape": ["square", "circle", "triangle"],
            "degrees": [360, 360, 180],
            "sides": [4.0, float("nan"), 3.0],
        }
    )

    tm.assert_frame_equal(df_nmsp, df_expected)
    tm.assert_frame_equal(df_iter, df_expected)

