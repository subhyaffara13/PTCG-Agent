
def bcoo_squeeze(arr: BCOO, *, dimensions: Sequence[int]) -> BCOO:
  """Sparse implementation of :func:`jax.lax.squeeze`.

  Squeeze any number of size 1 dimensions from an array.

  Args:
    arr: BCOO array to be reshaped.
    dimensions: sequence of integers specifying dimensions to squeeze.

  Returns:
    out: reshaped array.
  """
  dimensions = tuple(canonicalize_axis(dim, arr.ndim) for dim in dimensions)
  if any(arr.shape[dim] != 1 for dim in dimensions):
    raise ValueError("cannot select an axis to squeeze out which has size not equal to one, "
                     f"got shape={arr.shape} and {dimensions=}")
  batch_dims = tuple(d for d in dimensions if d < arr.n_batch)
  sparse_dims = np.array([i for i in range(arr.n_sparse)
                          if i + arr.n_batch not in dimensions], dtype=int)
  dense_dims = tuple(d - arr.n_sparse + 1 for d in dimensions
                     if d >= arr.n_batch + arr.n_sparse)
  data_out = lax.squeeze(arr.data, batch_dims + dense_dims)
  indices_out = lax.squeeze(arr.indices[..., sparse_dims], batch_dims)
  out_shape = tuple(s for i, s in enumerate(arr.shape) if i not in dimensions)
  return BCOO((data_out, indices_out), shape=out_shape,
              indices_sorted=arr.indices_sorted, unique_indices=arr.unique_indices)

