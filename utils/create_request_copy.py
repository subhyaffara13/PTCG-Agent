
def create_request_copy(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": _safe_get_request_headers(request).copy(),
        "cookies": request.cookies,
        "query_params": dict(request.query_params),
    }


def create_request_copy(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": _safe_get_request_headers(request).copy(),
        "cookies": request.cookies,
        "query_params": dict(request.query_params),
    }

