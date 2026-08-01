
def _is_exception_related_to_db(e: Exception) -> bool:
    """
    Returns True if the exception is related to the DB
    """

    import httpx
    from prisma.errors import PrismaError

    return isinstance(e, (PrismaError, httpx.ConnectError, httpx.TimeoutException))

