
def test_request_headers(responder, read_method, httpserver, storage_options):
    expected = pd.DataFrame({"a": ["b"]})
    default_headers = ["Accept-Encoding", "Host", "Connection", "User-Agent"]
    if "gz" in responder.__name__:
        extra = {"Content-Encoding": "gzip"}
        if storage_options is None:
            storage_options = extra
        else:
            storage_options |= extra
    else:
        extra = None
    expected_headers = set(default_headers).union(
        storage_options.keys() if storage_options else []
    )
    httpserver.serve_content(content=responder(expected), headers=extra)
    result = read_method(httpserver.url, storage_options=storage_options)
    tm.assert_frame_equal(result, expected)

    request_headers = dict(httpserver.requests[0].headers)
    for header in expected_headers:
        exp = request_headers.pop(header)
        if storage_options and header in storage_options:
            assert exp == storage_options[header]
    # No extra headers added
    assert not request_headers

