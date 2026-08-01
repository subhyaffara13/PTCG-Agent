
def do_one(*rules: Callable[[_T], _T]) -> Callable[[_T], _T]:
    """ Try each of the rules until one works. Then stop. """
    def do_one_rl(expr: _T) -> _T:
        for rl in rules:
            result = rl(expr)
            if result != expr:
                return result
        return expr
    return do_one_rl


def do_one(*brules):
    """ Execute one of the branching rules """
    def do_one_brl(expr):
        yielded = False
        for brl in brules:
            for nexpr in brl(expr):
                yielded = True
                yield nexpr
            if yielded:
                return
    return do_one_brl

