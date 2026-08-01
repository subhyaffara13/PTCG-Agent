
def contract_metric(t, g):
    if isinstance(t, TensExpr):
        return t.contract_metric(g)
    return t

