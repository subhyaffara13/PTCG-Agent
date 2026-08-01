
def _ensure_poly(p: DimSize,
                 operation_name: str,
                 scope: SymbolicScope) -> _DimExpr:
  if isinstance(p, _DimExpr):
    scope._check_same_scope(p, when=f"for operation {operation_name}")
    return p
  if _convertible_to_int(p):
    return _DimExpr(((_DimTerm_one, op.index(p)),), scope)
  raise TypeError(f"Symbolic dimension {operation_name} not supported for {p}.")

