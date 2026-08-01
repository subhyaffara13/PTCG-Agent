
def _rewrite_hyperbolics_as_exp(expr):
    return expr.xreplace({h: h.rewrite(exp)
        for h in expr.atoms(HyperbolicFunction)})

