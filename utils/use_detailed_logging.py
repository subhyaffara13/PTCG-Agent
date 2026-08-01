
def use_detailed_logging(module: ir.Module) -> bool:
  """Returns 'true' if detailed logging should be enabled for 'module'."""
  bound = _COMPILER_DETAILED_LOGGING_MIN_OPS.value
  return _walk_operations(module.operation, bound) < 0

