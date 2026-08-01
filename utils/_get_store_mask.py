
def _get_store_mask(
    *,
    grid_id: jnp.ndarray,
    group_metadata: GroupMetadata,
    tm: int,
    tn: int,
) -> jnp.ndarray:
  """Mask for rows that belong to the current group in the current tile."""
  group_offsets, group_ids, m_tile_ids = group_metadata[:3]
  group_id = group_ids[grid_id]
  group_start = group_offsets[group_id]
  group_end = group_offsets[group_id + 1]
  m_id = m_tile_ids[grid_id] * tm
  iota = jax.lax.broadcasted_iota(jnp.int32, (tm, tn), 0) + m_id
  return jnp.logical_and(iota >= group_start, iota < group_end)

