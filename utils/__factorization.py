
def _Factorization(predicate, expr, assumptions):
    if predicate in expr.predicates:
        return True

