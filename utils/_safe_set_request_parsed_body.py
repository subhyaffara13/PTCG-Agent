
def _safe_set_request_parsed_body(
    request: Optional[Request],
    parsed_body: dict,
) -> None:
    try:
        if request is None:
            return
        request.scope["parsed_body"] = (tuple(parsed_body.keys()), parsed_body)
    except Exception as e:
        verbose_proxy_logger.debug(
            "Unexpected error setting request parsed body - {}".format(e)
        )

