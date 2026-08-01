
def _sharding_constraint_batcher(
    axis_data, vals_in, dims_in, sharding, layout, context_mesh,
    unconstrained_dims):
  x, = vals_in
  d, = dims_in
  if d is None:
    out = sharding_constraint_p.bind(
        x, sharding=sharding, layout=layout, context_mesh=context_mesh,
        unconstrained_dims=unconstrained_dims)
    return out, None

  if axis_data.spmd_name is not None and isinstance(sharding, NamedSharding):
    used = {n for ns in sharding.spec
            for n in (ns if isinstance(ns, tuple) else (ns,))}
    if set(axis_data.spmd_name) & used:
      raise ValueError(f"vmap spmd_axis_name {axis_data.spmd_name} cannot appear in "
                       "with_sharding_constraint spec, but got spec "
                       f"{sharding.spec}")
  unconstrained_dims = {ud + (d <= ud) for ud in unconstrained_dims}
  if axis_data.spmd_name is None:
    unconstrained_dims.add(d)

  vmapped_sharding = _pjit_batcher_for_sharding(
      sharding, d, axis_data.spmd_name, context_mesh, x.ndim)
  if unconstrained_dims and isinstance(vmapped_sharding, NamedSharding):
    new_spec = list(vmapped_sharding.spec) + [None] * (x.ndim - len(vmapped_sharding.spec))
    for u in unconstrained_dims:
      new_spec[u] = PartitionSpec.UNCONSTRAINED
    vmapped_sharding = NamedSharding(
        vmapped_sharding.mesh, PartitionSpec(*new_spec))

  vmapped_layout = (get_layout_for_vmap(d, layout) if layout is not None else
                    layout)

  y = sharding_constraint_p.bind(
      x,
      sharding=vmapped_sharding,
      layout=vmapped_layout,
      context_mesh=context_mesh,
      unconstrained_dims=frozenset(unconstrained_dims))
  return y, d

