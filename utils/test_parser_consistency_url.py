
def test_parser_consistency_url(parser, httpserver):
    httpserver.serve_content(content=xml_default_nmsp)

    df_xpath = read_xml(StringIO(xml_default_nmsp), parser=parser)
    df_iter = read_xml(
        BytesIO(xml_default_nmsp.encode()),
        parser=parser,
        iterparse={"row": ["shape", "degrees", "sides"]},
    )

    tm.assert_frame_equal(df_xpath, df_iter)

