
def _log_llm_api_exception(e: Exception) -> None:
    if (
        getattr(e, "status_code", None) == 499
        and getattr(e, "detail", None) == _CLIENT_DISCONNECT_DETAIL
    ):
        verbose_proxy_logger.info(
            "litellm.proxy.proxy_server._handle_llm_api_exception(): client disconnected, upstream LLM request cancelled"
        )
        return
    verbose_proxy_logger.exception(
        f"litellm.proxy.proxy_server._handle_llm_api_exception(): Exception occured - {str(e)}"
    )

