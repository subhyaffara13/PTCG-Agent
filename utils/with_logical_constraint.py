
def with_logical_constraint(
  x: ArrayPytree,
  logical_axis_resources: LogicalPartitionSpecPytree,
  rules: LogicalRules | None = None,
  mesh: jax.sharding.Mesh | None = None,
  fallback: RulesFallback = RulesFallback.AXIS_IS_UNSHARDED,
):
  """Version of jit's with_sharding_constraint that uses logical axis names."""
  # If no axis binding is set, this is a no-op.
  if rules is None:
    rules = get_logical_axis_rules()
  if not rules or logical_axis_resources is None:
    return x
  # Translate logical names to mesh assignments.
  return jax.tree_util.tree_map(
    functools.partial(
      _with_sharding_constraint_one_fallback,
      fallback=fallback,
      rules=rules,
      mesh=mesh,
    ),
    logical_axis_resources,
    x,
    is_leaf=_is_logical_spec,
  )

