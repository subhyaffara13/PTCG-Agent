
def _has_omitted_header(headers: Headers, header: str) -> bool:
    header = header.lower()
    return any(key.lower() == header and isinstance(value, Omit) for key, value in headers.items())

