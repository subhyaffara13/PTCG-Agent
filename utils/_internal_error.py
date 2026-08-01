
def _internal_error(
    log_message: str, exc: Exception, default_detail: str
) -> HTTPException:
    """
    Build a 500 HTTPException with a generic, caller-safe `detail` while
    logging the actual exception server-side. Avoids leaking internal Prisma /
    DB details (table names, columns, connection metadata) to API callers.
    """
    verbose_proxy_logger.exception(log_message, exc)
    return HTTPException(status_code=500, detail=default_detail)

