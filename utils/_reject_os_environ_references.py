
def _reject_os_environ_references(params: dict) -> None:
    """
    Validate that the provided params do not contain any ``os.environ/``
    references. Values with that prefix are expected to come only from
    server-side configuration (already resolved before reaching here). If a
    request-supplied value still carries the prefix, raise ``HTTPException``.
    """
    if not isinstance(params, dict):
        return

    stack: list[object] = [params]
    seen: set[int] = {id(params)}

    while stack:
        src = stack.pop()
        if isinstance(src, dict):
            values: Iterable[object] = src.values()
        elif isinstance(src, list):
            values = src
        else:
            continue

        for value in values:
            if isinstance(value, str) and value.startswith("os.environ/"):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Environment variable references are not permitted in request parameters."
                    },
                )
            if isinstance(value, (dict, list)) and id(value) not in seen:
                seen.add(id(value))
                stack.append(value)

