import json

def giveup(e):
    result = not (
        isinstance(e, ProxyException)
        and getattr(e, "message", None) is not None
        and isinstance(e.message, str)
        and "Max parallel request limit reached" in e.message
    )

    if (
        general_settings.get("disable_retry_on_max_parallel_request_limit_error")
        is True
    ):
        return True  # giveup if queuing max parallel request limits is disabled

    if result:
        verbose_proxy_logger.debug(json.dumps({"event": "giveup", "exception": str(e)}))
    return result

