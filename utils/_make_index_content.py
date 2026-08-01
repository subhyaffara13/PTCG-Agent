
def _make_index_content(
    response: Response, cache_link_parsing: bool = True
) -> IndexContent:
    encoding = _get_encoding_from_headers(response.headers)
    return IndexContent(
        response.content,
        response.headers["Content-Type"],
        encoding=encoding,
        url=response.url,
        cache_link_parsing=cache_link_parsing,
    )

