
def MS_elements(predicate, expr, assumptions):
    """ Matrix Slice elements. """
    return ask(predicate(expr.parent), assumptions)

