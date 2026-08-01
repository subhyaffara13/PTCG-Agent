
def getAlternatives(n):
    if isinstance(n, ast.If):
        return [n.body]
    elif isinstance(n, ast.Try):
        return [n.body + n.orelse] + [[hdl] for hdl in n.handlers]
    elif sys.version_info >= (3, 10) and isinstance(n, ast.Match):
        return [mc.body for mc in n.cases]

