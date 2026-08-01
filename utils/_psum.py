
def _psum(xs: Any) -> Any:
  return jax.tree.map(lambda x: jnp.sum(x, dtype=x.dtype, axis=0), xs)


def _psum(x, axis_name, *, axis_index_groups, is_async):
  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)
  if not axis_name:
    return x
  if any(isinstance(axis, int) for axis in axis_name) and axis_index_groups is not None:
    raise ValueError("axis_index_groups only supported for sums over just named axes")
  _validate_reduce_axis_index_groups(axis_index_groups)
  leaves, treedef = tree_util.tree_flatten(x)
  leaves = [lax.convert_element_type(l, np.int32)
            if dtypes.dtype(l) == np.bool_ else l for l in leaves]
  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  # handle the constant case specially
  if all(not isinstance(leaf, core.Tracer) for leaf in leaves):
    named_axes, pos_axes = axes_partition = [], []
    for axis in axis_name:
      axes_partition[isinstance(axis, int)].append(axis)
    def pos_reduce(x):
      if not pos_axes:
        return x
      return lax.reduce_sum(x, [canonicalize_axis(axis, getattr(x, 'ndim', 0))
                                for axis in pos_axes])
    if axis_index_groups is not None:
      assert not pos_axes
      size = len(axis_index_groups[0])
    else:
      size = math.prod([core.get_axis_env().axis_size(name) for name in named_axes])
    out_flat = tuple(lax._const(leaf, size) * pos_reduce(leaf) for leaf in leaves)
  else:
    if config._check_vma.value:
      out_flat = [bind_psum_invariant(leaf, axes=tuple(axis_name),
                                      axis_index_groups=axis_index_groups,
                                      is_async=is_async)
                  for leaf in leaves]
    else:
      prim = psum_start_p if is_async else psum_p
      out_flat = [prim.bind(leaf, axes=tuple(axis_name),
                              axis_index_groups=axis_index_groups)
                  for leaf in leaves]
  return tree_util.tree_unflatten(treedef, out_flat)

