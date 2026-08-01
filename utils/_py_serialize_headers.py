
def _py_serialize_headers(status_line: str, headers: "CIMultiDict[str]") -> bytes:
    _safe_header(status_line)
    headers_gen = (_safe_header(k) + ": " + _safe_header(v) for k, v in headers.items())
    line = status_line + "\r\n" + "\r\n".join(headers_gen) + "\r\n\r\n"
    return line.encode("utf-8")

