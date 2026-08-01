
def null_safe(rule: Callable[[_T], _T | None]) -> Callable[[_T], _T]:
    """ Return original expr if rule returns None """
    def null_safe_rl(expr: _T) -> _T:
        result = rule(expr)
        if result is None:
            return expr
        return result
    return null_safe_rl

