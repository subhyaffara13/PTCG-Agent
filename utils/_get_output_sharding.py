
def _get_output_sharding(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> OutputSharding:
    """Get the output sharding for the given op."""
    op_info = dtensor.DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)
    dtensor.DTensor._op_dispatcher.sharding_propagator.propagate(op_info)
    output_sharding = op_info.output_sharding
    if output_sharding is None:
        raise AssertionError("output sharding should not be None")
    return output_sharding


def _get_output_sharding(shardings):
  lhs, rhs = shardings[0], shardings[1]
  batch_spec, m_spec, _ = lhs.spec
  _, n_spec, _ = rhs.spec

  if _enable_reduce_scatter(lhs, rhs):
    return [NamedSharding(lhs.mesh, P(*lhs.spec))]

  output_specs = (batch_spec, m_spec)
  # If the m and n specs are overlapping, we cannot keep both -
  # we (arbitrarily) pick m and replicate for n.
  output_specs += (None,) if _are_specs_overlapping(m_spec, n_spec) else (n_spec,)
  return [NamedSharding(lhs.mesh, P(*output_specs))]

