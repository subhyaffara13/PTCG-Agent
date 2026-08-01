
def get_hint(v: sympy.Expr | int) -> int:
    if isinstance(v, int):
        return v
    else:
        return V.graph.sizevars.optimization_hint(v)


def get_hint(x: int | torch.SymInt) -> int | None:
    if isinstance(x, int):
        return x
    assert isinstance(x, torch.SymInt)
    return x.node.hint if x.node.has_hint() else None


def get_hint(x: int | torch.SymInt) -> int | None:
    if isinstance(x, int):
        return x
    assert isinstance(x, torch.SymInt)
    if not x.node.has_hint():
        return None
    return x.node.hint

