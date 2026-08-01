
def all_gather_invariant(x, axis_name, *, axis: int = 0, tiled: bool = False):
  """Gather values of x across all replicas.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  all_gather_invariant differs from all_gather in the following ways:

  * all_gather_invariant is Varying -> Invariant.
    For example: `out: f32[8] = all_gather_invariant(inp: f32[4]{V: x}, 'x')`
    where the size of mesh axis `x` is 2.
    While all_gather is Varying -> Varying.

  * all_gather_invariant transposes to dynamic_slice which is
    Invariant -> Varying. While all_gather transposes to reduce_scatter
    which is Varying -> Varying.
  """
  if not isinstance(axis_name, tuple):
    axis_name = (axis_name,)
  if not axis_name:
    return x
  axis_size = _axis_size(axis_name, None)
  axes_ = frozenset(axis_name)
  def bind(leaf):
    in_vma = core.typeof(leaf).mat.varying
    if config.auto_pcast.value and (vary_names := axes_ - in_vma):
      leaf = pvary(leaf, tuple(vary_names))
    return all_gather_invariant_p.bind(
        leaf,
        all_gather_dimension=canonicalize_axis(axis, np.ndim(leaf) if tiled else
                                               np.ndim(leaf) + 1),
        axis_name=axis_name, axis_size=axis_size, tiled=tiled)
  return tree_util.tree_map(bind, x)

