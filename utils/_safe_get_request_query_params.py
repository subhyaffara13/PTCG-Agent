
def _safe_get_request_query_params(request: Optional[Request]) -> Dict:
    if request is None:
        return {}
    try:
        if hasattr(request, "query_params"):
            return dict(request.query_params)
        return {}
    except Exception as e:
        verbose_proxy_logger.debug(
            "Unexpected error reading request query params - {}".format(e)
        )
        return {}

