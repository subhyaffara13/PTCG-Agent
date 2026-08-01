
def get_api_key_from_custom_header(
    request: Request, custom_litellm_key_header_name: str
) -> str:
    """
    Get API key from custom header

    Args:
        request (Request): Request object
        custom_litellm_key_header_name (str): Custom header name

    Returns:
        Optional[str]: API key
    """
    api_key: str = ""
    # use this as the virtual key passed to litellm proxy
    custom_litellm_key_header_name = custom_litellm_key_header_name.lower()
    _headers = {k.lower(): v for k, v in request.headers.items()}
    verbose_proxy_logger.debug(
        "searching for custom_litellm_key_header_name= %s, in headers=%s",
        custom_litellm_key_header_name,
        _headers,
    )
    custom_api_key = _headers.get(custom_litellm_key_header_name)
    if custom_api_key:
        api_key = _get_bearer_token(api_key=custom_api_key)
        verbose_proxy_logger.debug(
            "Found custom API key using header: {}, setting api_key={}".format(
                custom_litellm_key_header_name, abbreviate_api_key(api_key)
            )
        )
    else:
        verbose_proxy_logger.exception(
            f"No LiteLLM Virtual Key pass. Please set header={custom_litellm_key_header_name}: Bearer <api_key>"
        )
    return api_key

