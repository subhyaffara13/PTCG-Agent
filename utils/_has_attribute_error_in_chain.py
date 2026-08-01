
def _has_attribute_error_in_chain(exc: Exception) -> bool:
    """Walk the exception chain to find an AttributeError at any depth.

    Checks __cause__, __context__, and the litellm-specific original_exception
    attribute iteratively. Depth is capped at DEFAULT_MAX_RECURSE_DEPTH to
    avoid infinite loops from circular exception references.
    """
    stack: list[BaseException] = [exc]
    seen: set[int] = set()
    depth = 0
    while stack and depth < DEFAULT_MAX_RECURSE_DEPTH:
        current = stack.pop()
        exc_id = id(current)
        if exc_id in seen:
            continue
        seen.add(exc_id)
        if isinstance(current, AttributeError):
            return True
        for attr in ("__cause__", "__context__", "original_exception"):
            inner = getattr(current, attr, None)
            if inner is not None and isinstance(inner, BaseException):
                stack.append(inner)
        depth += 1
    return False

