
def psend(x, axis_name, perm):
  """Perform a collective send according to the permutation ``perm``.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  This function is an analog of the Send HLO.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    perm: list of pairs of ints, representing ``(source_index,
      destination_index)`` pairs that encode how the mapped axis named
      ``axis_name`` should be shuffled. The integer values are treated as
      indices into the mapped axis ``axis_name``. Any two pairs should not have
      the same source index or the same destination index. For each index of the
      axis ``axis_name`` that does not correspond to a destination index in
      ``perm``, the corresponding values in the result are filled with zeros of
      the appropriate type. The semantics here are platform-specific, and for
      GPU they correspond to NCCL send.

  Returns:
    A compiler token that can be used by precv and lax.optimzation_barrier to
    enforce ordering of collective ops.
  """
  axis_name = tuple(axis_name) if isinstance(axis_name, (list, tuple)) else (axis_name,)

  def bind(leaf):
    leaf = insert_collective_pvary(axis_name, leaf)
    return psend_p.bind(leaf, axis_name=axis_name, perm=tuple(map(tuple, perm)))

  return tree_util.tree_map(bind, x)

