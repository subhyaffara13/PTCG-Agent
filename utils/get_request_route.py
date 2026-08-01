
def get_request_route(request: Request) -> str:
    """
    Resolve the request route from the ASGI scope, with ``root_path`` stripped.

    Prefer this over ``request.url.path`` for any auth, ACL, routing, or
    audit-log decision: Starlette reconstructs ``url.path`` by interpolating
    the Host header into a URL string and re-parsing with ``urlsplit``, so a
    malformed Host (e.g. ``localhost/?x=1``) collapses ``url.path`` to ``"/"``
    while FastAPI continues to dispatch on ``scope["path"]``. ``scope["path"]``
    is uvicorn's parse of the HTTP request line and matches the actual
    handler, so it's the authoritative route.

    Also normalizes sub-path deployments by stripping ``scope["root_path"]``
    e.g. ``/genai/chat/completions`` -> ``/chat/completions``.
    """
    try:
        scope = request.scope
        if not isinstance(scope, dict):
            return str(request.url.path)
        raw_path: str = str(scope.get("path", request.url.path))
        root_path: str = str(
            scope.get("app_root_path", scope.get("root_path", ""))
        ).rstrip("/")
        if not isinstance(raw_path, str):
            return str(request.url.path)
        # Strip root_path only when it matches whole path segments — guarding
        # against sibling paths like "/apifoo" being truncated under
        # root_path="/api". Trailing slashes on root_path are stripped above,
        # so bare "/" or "/prefix/" still leave the leading "/" intact.
        if root_path and (
            raw_path == root_path or raw_path.startswith(root_path + "/")
        ):
            stripped = raw_path[len(root_path) :]
            return stripped or "/"
        return raw_path
    except Exception as e:
        verbose_proxy_logger.debug(
            f"error on get_request_route: {str(e)}, defaulting to request.url.path={request.url.path}"
        )
        return str(request.url.path)

