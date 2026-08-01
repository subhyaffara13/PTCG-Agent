
def exhaust(rule: Callable[[_T], _T]) -> Callable[[_T], _T]:
    """ Apply a rule repeatedly until it has no effect """
    def exhaustive_rl(expr: _T) -> _T:
        new, old = rule(expr), expr
        while new != old:
            new, old = rule(new), new
        return new
    return exhaustive_rl


def exhaust(brule):
    """ Apply a branching rule repeatedly until it has no effect """
    def exhaust_brl(expr):
        seen = {expr}
        for nexpr in brule(expr):
            if nexpr not in seen:
                seen.add(nexpr)
                yield from exhaust_brl(nexpr)
        if seen == {expr}:
            yield expr
    return exhaust_brl

