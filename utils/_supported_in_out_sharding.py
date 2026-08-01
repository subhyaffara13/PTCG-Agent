
def _supported_in_out_sharding(lhs_sharding, rhs_sharding, out_sharding, reduce_scatter_dim):
  use_all_reduce = _enable_all_reduce(lhs_sharding, rhs_sharding)

  batch_spec, m_spec, k_spec = lhs_sharding.spec
  batch_spec_rhs, n_spec, _ = rhs_sharding.spec

  # This is checked by the caller, assert here for documentation.
  assert batch_spec == batch_spec_rhs

  def named_sharding(lhs_specs, rhs_specs, out_specs):
    lhs = NamedSharding(lhs_sharding.mesh, P(*lhs_specs))
    rhs = NamedSharding(rhs_sharding.mesh, P(*rhs_specs))
    out = NamedSharding(lhs_sharding.mesh, P(*out_specs))
    return ((lhs, rhs, lhs, rhs), [out])

  if reduce_scatter_dim == 1:
    lhs_specs = (batch_spec, None, k_spec)
    rhs_specs = (batch_spec, n_spec, k_spec)
    out_specs = (batch_spec, k_spec, n_spec)
    return named_sharding(lhs_specs, rhs_specs, out_specs)

  if reduce_scatter_dim == 2:
    lhs_specs = (batch_spec, m_spec, k_spec)
    rhs_specs = (batch_spec, None, k_spec)
    out_specs = (batch_spec, m_spec, k_spec)
    return named_sharding(lhs_specs, rhs_specs, out_specs)

  if not use_all_reduce:
    k_spec = None

  if _are_specs_overlapping(m_spec, n_spec):
    # We have m and n specs that share an axis, so we can't keep both.
    # Let us keep the one that was inferred in the output.
    if n_spec == out_sharding.spec[2]:
      # Output has n spec, so we get rid of m.
      m_spec = None
    else:
      # Otherwise, we get rid of n.
      n_spec = None

  lhs_specs = (batch_spec, m_spec, k_spec)
  rhs_specs = (batch_spec, n_spec, k_spec)
  out_specs = (batch_spec, m_spec, n_spec)
  return named_sharding(lhs_specs, rhs_specs, out_specs)

