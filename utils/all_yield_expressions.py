
def all_yield_expressions(node: Node) -> list[tuple[YieldExpr, bool]]:
    v = YieldCollector()
    node.accept(v)
    return v.yield_expressions

