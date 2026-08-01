
def handle_exception_on_proxy(e: Exception) -> ProxyException:
    """
    Returns an Exception as ProxyException, this ensures all exceptions are OpenAI API compatible
    """
    from fastapi import status

    verbose_proxy_logger.exception(f"Exception: {e}")

    if isinstance(e, HTTPException):
        return ProxyException(
            message=getattr(e, "detail", f"error({str(e)})"),
            type=ProxyErrorTypes.internal_server_error,
            param=getattr(e, "param", "None"),
            code=getattr(e, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        )
    elif isinstance(e, ProxyException):
        return e
    _status_code = getattr(e, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return ProxyException(
        message=str(e),
        type=ProxyErrorTypes.internal_server_error,
        param=getattr(e, "param", "None"),
        code=_status_code,
    )

