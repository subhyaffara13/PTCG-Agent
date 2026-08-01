
def BM_elements(predicate, expr, assumptions):
    """ Block Matrix elements. """
    return all(ask(predicate(b), assumptions) for b in expr.blocks)

