
def _dir(
    *,
    globals_: dict[str, Any],
    imported_symbols: dict[str, lazy_imports_utils.LazyModule | Any],
) -> list[str]:
  """Module `__dir__` that lazy-imports symbols."""
  return list(globals_) + list(imported_symbols)

