
def has_body_headers(request: Request) -> bool:
    return any(
        k.lower() == b"content-length" or k.lower() == b"transfer-encoding"
        for k, v in request.headers
    )


def has_body_headers(request: Request) -> bool:
    return any(
        k.lower() == b"content-length" or k.lower() == b"transfer-encoding"
        for k, v in request.headers
    )

