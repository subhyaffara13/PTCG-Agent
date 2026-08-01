
def _apply_sharding(value, sharding, mesh):
  if isinstance(sharding, Format):
    return jax.lax.with_sharding_constraint(value, sharding)
  if mesh.are_all_axes_explicit:
    return jax.sharding.reshard(value, sharding)
  elif mesh.are_all_axes_auto:
    return jax.lax.with_sharding_constraint(value, sharding)
  else:
    raise ValueError(
        'Mesh must have all axes as Explicit or all axes as Auto. '
        f'Got mixed axis types: {mesh.axis_types}')

