
def _get_http_response_size(resp: Response) -> int | None:
    try:
        return int(resp.headers["content-length"])
    except (ValueError, KeyError, TypeError):
        return None

