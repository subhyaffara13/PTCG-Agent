
def _first_non_cancelled_cause(exc: BaseException) -> Optional[BaseException]:
    queue: List[BaseException] = [exc]
    while queue:
        current = queue.pop(0)
        nested = getattr(current, "exceptions", None)
        if nested:
            queue.extend(nested)
        elif not isinstance(current, asyncio.CancelledError):
            return current
    return None

