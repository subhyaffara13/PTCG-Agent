
def _extract_upstream_auth_failure(
    exc: BaseException,
) -> Optional[Tuple[int, Optional[str]]]:
    """Walk the exception tree looking for an HTTP 401/403 response from the
    upstream MCP server.

    The MCP SDK wraps transport errors in anyio ``ExceptionGroup`` objects and
    may chain through ``__cause__`` / ``__context__``. We inspect all of those
    layers for an ``httpx.Response``-bearing exception (typically
    ``httpx.HTTPStatusError``) and extract the status code and any upstream
    ``WWW-Authenticate`` header.

    Returns ``(status_code, www_authenticate)`` on match, else ``None``.
    """
    seen: Set[int] = set()
    stack: List[BaseException] = [exc]
    while stack:
        current = stack.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))

        response = getattr(current, "response", None)
        if response is not None:
            status_code = getattr(response, "status_code", None)
            if isinstance(status_code, int) and status_code in (401, 403):
                www_authenticate: Optional[str] = None
                headers = getattr(response, "headers", None)
                if headers is not None:
                    try:
                        www_authenticate = headers.get("www-authenticate")
                    except Exception:
                        www_authenticate = None
                return status_code, www_authenticate

        # anyio / PEP 654 ExceptionGroup
        sub_exceptions = getattr(current, "exceptions", None)
        if sub_exceptions:
            stack.extend(sub_exceptions)

        if current.__cause__ is not None:
            stack.append(current.__cause__)
        if (
            current.__context__ is not None
            and current.__context__ is not current.__cause__
        ):
            stack.append(current.__context__)

    return None

