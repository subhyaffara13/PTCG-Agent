
def _list_terms(expr):
    if not isinstance(expr, Add):
        return [expr]

    return expr.args

