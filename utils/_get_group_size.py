
def _get_group_size(group: ProcessGroup | None) -> int:
    """Get a given group's world size."""
    if group is GroupMember.WORLD or group is None:
        default_pg = _get_default_group()
        return default_pg.size()
    return group.size()


def _get_group_size(
    *, grid_id: jnp.ndarray, group_metadata: GroupMetadata
) -> jnp.ndarray:
  """Calculate the number of rows in the current group."""
  group_offsets, group_ids = group_metadata[:2]
  group_id = group_ids[grid_id]
  group_start = group_offsets[group_id]
  group_end = group_offsets[group_id + 1]
  return group_end - group_start

