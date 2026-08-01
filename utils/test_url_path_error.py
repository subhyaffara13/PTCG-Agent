
def test_url_path_error(parser, httpserver, xml_file):
    with open(xml_file, encoding="utf-8") as f:
        httpserver.serve_content(content=f.read())
        with pytest.raises(
            ParserError, match=("iterparse is designed for large XML files")
        ):
            read_xml(
                httpserver.url,
                parser=parser,
                iterparse={"row": ["shape", "degrees", "sides", "date"]},
            )

