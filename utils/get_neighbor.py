
def get_neighbor(
    idx: jax.Array, mesh: jax.sharding.Mesh, axis_name: str, *, direction: str
) -> tuple[jax.Array, ...]:
  """Helper function that computes the mesh indices of a neighbor."""
  axis_names = mesh.axis_names
  which_axis = axis_names.index(axis_name)
  mesh_index = [
      idx if i == which_axis else lax.axis_index(a)
      for i, a in enumerate(axis_names)
  ]
  axis_size = lax.axis_size(axis_name)
  if direction == "right":
    next_idx = lax.rem(idx + 1, axis_size)
  else:
    left = idx - 1
    next_idx = jnp.where(left < 0, left + axis_size, left)
  mesh_index[which_axis] = next_idx
  return tuple(mesh_index)

