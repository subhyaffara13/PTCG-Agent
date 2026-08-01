
def _has_header(headers: Headers, header: str) -> bool:
    header = header.lower()
    return any(key.lower() == header for key in headers)


def _has_header(headers: Headers, header: str) -> bool:
    header = header.lower()
    return any(key.lower() == header for key in headers)

