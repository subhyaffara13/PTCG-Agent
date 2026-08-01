
def intern_string(s: str | None) -> int:
    if s is None:
        return -1

    r = INTERN_TABLE.get(s)
    if r is None:
        r = len(INTERN_TABLE)
        INTERN_TABLE[s] = r
        torch._logging._internal.trace_structured(
            "str", lambda: (s, r), suppress_context=True
        )
    return r

