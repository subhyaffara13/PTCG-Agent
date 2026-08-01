
def has_indirect_access(memory_expr: sympy.Expr) -> bool:
    """
    Check if this memory expression has any indirect indexing.
    """
    return any(symbol_is_type(s, SymT.INDIRECT) for s in memory_expr.free_symbols)

