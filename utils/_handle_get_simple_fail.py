
def _handle_get_simple_fail(
    link: Link,
    reason: str | Exception,
    meth: Callable[..., None] | None = None,
) -> None:
    if meth is None:
        meth = logger.debug
    meth("Could not fetch URL %s: %s - skipping", link, reason)

