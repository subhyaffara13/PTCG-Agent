
def test_wrong_url(parser, httpserver):
    httpserver.serve_content("NOT FOUND", code=404)
    try:
        with pytest.raises(HTTPError, match=("HTTP Error 404: NOT FOUND")) as err:
            read_xml(httpserver.url, xpath=".//book[count(*)=4]", parser=parser)
    finally:
        if isinstance(err.value, HTTPError):
            # Has a file-like handle that we can close
            # https://docs.python.org/3/library/urllib.error.html#urllib.error.HTTPError
            err.value.close()

