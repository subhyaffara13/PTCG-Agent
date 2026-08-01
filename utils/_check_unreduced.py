
def _check_unreduced(error_type, mesh, manual_axes, specs):
  from jax._src.hijax import HiPspec
  prefix = 'in' if error_type == SpecErrorType.input else 'out'
  full_manual = frozenset(mesh.axis_names) == manual_axes
  specs_flat, _ = tree_flatten(specs)
  for s in specs_flat:
    if isinstance(s, HiPspec):
      continue  # TODO(mattjj,yashkatariya): add user validation method
    if not s.unreduced and not s.reduced:
      continue
    if not full_manual:
      raise NotImplementedError(
          f"unreduced/reduced can only be passed to {prefix}_specs when"
          " shard_map is in full manual mode. Got mesh axis names"
          f" {mesh.axis_names}, manual_axes: {manual_axes}, specs: {s}. Please"
          " file a bug at https://github.com/jax-ml/jax/issues.")
    if not all(mesh._name_to_type[u] == AxisType.Explicit for u in s.unreduced):
      raise ValueError(
          f"unreduced in {prefix}_specs {s} can only be used when the mesh"
          " passed to shard_map contains axis names all of type `Explicit`."
          f" Got mesh {mesh}")
    if not all(mesh._name_to_type[u] == AxisType.Explicit for u in s.reduced):
      raise ValueError(
          f"reduced in {prefix}_specs {s} can only be used when the mesh"
          " passed to shard_map contains axis names all of type `Explicit`."
          f" Got mesh {mesh}")

