
def find_walrus_targets(expr: Expression) -> set[SymbolNode]:
    """Return the symbols reassigned via a walrus expression within 'expr'.

    Walrus (':=') is the only way to rebind a variable in the middle of evaluating
    an expression, so this is the complete set of in-expression reassignments.
    """
    collector = WalrusTargetCollector()
    expr.accept(collector)
    return collector.targets

