
def _logical_to_mesh_axes(
    array_dim_names: Sequence[str | None] | None,
    rules: LogicalRules | None = None,
) -> list[_UnassignedAxis | None | str | tuple[str, ...]] | None:
  """Same as logical_to_mesh_axes, but doesn't fill in _unassigned_axis."""
  if array_dim_names is None:
    return None
  if rules is None:
    rules = get_logical_axis_rules()
  axis_name_counts = collections.Counter(array_dim_names)
  # None and special values such as PartitionSpec.UNCONSTRAINED can appear more
  # then once.
  dups = tuple(
      k for k, v in axis_name_counts.items() if v > 1 and isinstance(k, str)
  )
  if dups:
    raise ValueError(
      f'Unsupported: Dimensions {dups} occur more than once in array names.'
    )
  if not isinstance(rules, (tuple, list)):
    raise ValueError('Unknown axis rule specification type.')
  # We assign mesh axes using a priority based ruleset over logical axis names.
  result: list[_UnassignedAxis | None | str | tuple[str, ...]]
  result = [
      (_unassigned_axis if isinstance(name, str) else name)
      for name in array_dim_names
  ]
  for rule_model_name, rule_mesh_names in rules:
    if rule_model_name in array_dim_names:
      pos = array_dim_names.index(rule_model_name)
      if (
        _mesh_assignment_free(rule_mesh_names, result)
        and result[pos] == _unassigned_axis
      ):
        result[pos] = rule_mesh_names
  return result

