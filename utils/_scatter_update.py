
def _scatter_update(x: ArrayLike, idx: Index | tuple[Index, ...],
                    y: ArrayLike, scatter_op: Callable[..., Array],
                    indices_are_sorted: bool, unique_indices: bool,
                    mode: slicing.GatherScatterMode | str | None = None,
                    normalize_indices: bool = True,
                    out_sharding: NamedSharding | None = None):
  """Helper for indexed updates.

  Computes the value of x that would result from computing::
    x[idx] op= y
  except in a pure functional way, with no in-place updating.

  Args:
    x: ndarray to be updated.
    idx: None, an integer, a slice, an ellipsis, an ndarray with integer dtype,
      or a tuple of those indicating the locations of `x` into which to scatter-
      update the values in `y`.
    y: values to be scattered.
    scatter_op: callable, one of lax.scatter, lax.scatter_add, lax.scatter_min,
      or lax_scatter_max.
    indices_are_sorted: whether `idx` is known to be sorted
    unique_indices: whether `idx` is known to be free of duplicates

  Returns:
    An ndarray representing an updated `x` after performing the scatter-update.
  """
  x = jnp.asarray(x)
  if (isinstance(y, int) and np.issubdtype(x.dtype, np.integer) and
      np.iinfo(x.dtype).min <= y <= np.iinfo(x.dtype).max):
    y = jnp.asarray(y, dtype=x.dtype)
  else:
    y = jnp.asarray(y)

  # XLA gathers and scatters are very similar in structure; the scatter logic
  # is more or less a transpose of the gather equivalent.
  indexer = indexing.NDIndexer.from_raw_indices(idx, x.shape).expand_bool_indices()
  dynamic_idx, treedef = tree_util.tree_flatten(indexer)
  dynamic_idx = tuple(dynamic_idx)
  internal_scatter = partial(
      _scatter_impl, scatter_op=scatter_op, treedef=treedef,
      indices_are_sorted=indices_are_sorted,
      unique_indices=unique_indices, mode=mode,
      normalize_indices=normalize_indices)
  if out_sharding is not None:
    return auto_axes(internal_scatter, out_sharding=out_sharding,
                     axes=out_sharding.mesh.explicit_axes
                     )(x, y, dynamic_idx)
  return internal_scatter(x, y, dynamic_idx)

