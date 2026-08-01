
def _prepare_pmap(fun, axis_name, static_broadcasted_argnums,
                      donate_argnums, in_axes, out_axes):
  # axis_size is an optional integer representing the global axis size.  The
  # aggregate size (across all processes) size of the mapped axis must match the
  # given value.
  check_callable(fun)
  axis_name = "_internal_pmap_axis_name" if axis_name is None else axis_name
  static_broadcasted_tuple = _ensure_index_tuple(static_broadcasted_argnums)
  donate_tuple = rebase_donate_argnums(
      _ensure_index_tuple(donate_argnums), static_broadcasted_tuple)

  if not all(type(l) is int for l in tree_leaves(in_axes)):
    raise TypeError("pmap in_axes must be an int, None, or (nested) container "
                    f"with those types as leaves, but got {in_axes}.")
  if not all(type(l) is int for l in tree_leaves(out_axes)):
    raise TypeError("pmap out_axes must be an int, None, or (nested) container "
                    f"with those types as leaves, but got {out_axes}.")

  return axis_name, static_broadcasted_tuple, donate_tuple

