
def write_request(request: Request, write: Writer) -> None:
    if request.http_version != b"1.1":
        raise LocalProtocolError("I only send HTTP/1.1")
    write(b"%s %s HTTP/1.1\r\n" % (request.method, request.target))
    write_headers(request.headers, write)

