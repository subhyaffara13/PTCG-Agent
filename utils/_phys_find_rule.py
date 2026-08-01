
def _phys_find_rule(primitive, avals: Sequence[core.AbstractValue]):
  """Finds the physicalization rule for a primitive."""
  if primitive in _physicalize_rules:
    return _physicalize_rules[primitive]

  # pyrefly: ignore[missing-attribute]
  fusion_types = {aval.dtype for aval in avals if _is_fusion_type(aval)}
  if len(fusion_types) == 0:
    return None
  elif len(fusion_types) > 1:
    raise ValueError(f"Multiple fusion types for primitive: {fusion_types}")
  fusion_type = fusion_types.pop()
  if primitive not in fusion_type._op_registry:
    raise ValueError(
        f"No implementation found for primitive {primitive} "
        f"for custom type {fusion_type}"
    )
  return fusion_type.get_op_rule(primitive)

