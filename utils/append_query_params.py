
def append_query_params(url: Optional[str], params: dict) -> str:
    from litellm._logging import verbose_proxy_logger

    verbose_proxy_logger.debug(f"url: {url}")
    verbose_proxy_logger.debug(f"params: {params}")
    if not isinstance(url, str) or url == "":
        # Preserve previous startup behavior when DATABASE_URL is absent.
        # Returning an empty string avoids urlparse type errors in test/dev flows.
        verbose_proxy_logger.warning(
            "append_query_params received empty or non-string URL, returning empty string"
        )
        return ""
    parsed_url = urlparse.urlparse(url)
    parsed_query = urlparse.parse_qs(parsed_url.query)
    parsed_query.update(params)
    encoded_query = urlparse.urlencode(parsed_query, doseq=True)
    modified_url = urlparse.urlunparse(parsed_url._replace(query=encoded_query))
    return modified_url  # type: ignore

