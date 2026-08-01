
def _core_variable_with_axes(
    scope,
    col: str,
    name: str,
    init_fn: Callable[..., Any],
    *init_args,
    axes: tuple[str, ...] | None = None,
    fallback: RulesFallback = RulesFallback.AXIS_IS_UNSHARDED,
    **init_kwargs,
):
  """Variant of flax core variable scope call with sharding constraints."""
  scope.reserve(name)
  if not scope.has_variable(col, name):
    if not scope.is_mutable_collection(col):
      raise flax.errors.ScopeVariableNotFoundError(name, col, scope.path_text)
    init_value = init_fn(*init_args, **init_kwargs)
    if axes is not None:
      init_value = with_sharding_constraint(init_value, axes, fallback=fallback)
    scope.put_variable(col, name, init_value)
  return PartitionedVariable(scope, col, name, axes, fallback)

