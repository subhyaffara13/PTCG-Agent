from typing import Any

def _smap(f: F, *, in_axes: int | None | InferFromArgs | tuple[Any, ...],
          out_axes: Any, axis_name: AxisName) -> F:
  if isinstance(axis_name, (list, tuple)):
    raise TypeError(
        f"smap axis_name should be a `str` or a `Hashable`, but got {axis_name}")
  if (in_axes is not None and in_axes is not Infer and
      not isinstance(in_axes, (int, tuple))):
    raise TypeError(
        "smap in_axes must be an int, None, jax.sharding.Infer, or a tuple of"
        " entries corresponding to the positional arguments passed to the"
        f" function, but got {in_axes}.")
  if (in_axes is not Infer and
      not all(isinstance(l, int) for l in tree_leaves(in_axes))):
    raise TypeError(
        "smap in_axes must be an int, None, jax.sharding.Infer, or (nested)"
        f" container with those types as leaves, but got {in_axes}.")
  if not all(isinstance(l, int) for l in tree_leaves(out_axes)):
    raise TypeError("smap out_axes must be an int, None, or (nested) container "
                    f"with those types as leaves, but got {out_axes}.")

  in_specs = (Infer if in_axes is Infer else
              tree_map(partial(_axes_to_pspec, axis_name), in_axes,
                       is_leaf=lambda x: x is None))
  out_specs = tree_map(partial(_axes_to_pspec, axis_name), out_axes,
                       is_leaf=lambda x: x is None)
  return _shard_map(f, mesh=None, in_specs=in_specs, out_specs=out_specs,
                    axis_names={axis_name}, check_vma=True, _smap=True)

