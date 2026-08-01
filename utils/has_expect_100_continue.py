
def has_expect_100_continue(request: "Request") -> bool:
    # https://tools.ietf.org/html/rfc7231#section-5.1.1
    # "A server that receives a 100-continue expectation in an HTTP/1.0 request
    # MUST ignore that expectation."
    if request.http_version < b"1.1":
        return False
    expect = get_comma_header(request.headers, b"expect")
    return b"100-continue" in expect

