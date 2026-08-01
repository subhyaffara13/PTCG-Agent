
def bcoo_reshape(mat: BCOO, *, new_sizes: Sequence[int],
                 dimensions: Sequence[int] | None = None,
                 sharding=None) -> BCOO:
  """Sparse implementation of :func:`jax.lax.reshape`.

  Args:
    operand: BCOO array to be reshaped.
    new_sizes: sequence of integers specifying the resulting shape. The size
      of the final array must match the size of the input. This must be specified
      such that batch, sparse, and dense dimensions do not mix.
    dimensions: optional sequence of integers specifying the permutation order of
      the input shape. If specified, the length must match ``operand.shape``.
      Additionally, dimensions must only permute among like dimensions of mat:
      batch, sparse, and dense dimensions cannot be permuted.

  Returns:
    out: reshaped array.
  """
  if (mat.indices.shape[:mat.n_batch] != mat.data.shape[:mat.n_batch] != mat.shape[:mat.n_batch]):
    # TODO(jakevdp) implement this case via broadcast_in_dim
    raise NotImplementedError("reshape of arrays with broadcasted batch dimensions.")

  batch_shape, sparse_shape, dense_shape = split_list(mat.shape, [mat.n_batch, mat.n_sparse])
  batch_perm, sparse_perm, dense_perm = _validate_permutation(
    mat.data, mat.indices, dimensions or tuple(range(mat.ndim)), mat.shape)
  batch_size = math.prod(batch_shape)
  sparse_size = math.prod(sparse_shape)

  cuml_shape = np.cumprod(new_sizes)
  if batch_size != 1 and batch_size not in cuml_shape:
    raise ValueError("bcoo_reshape: new shape cannot mix batch and sparse dimensions; "
                     f"got shape={mat.shape} new_shape={new_sizes} with n_batch={mat.n_batch}")
  if sparse_size != 1 and batch_size * sparse_size not in cuml_shape:
    raise ValueError("bcoo_reshape: new shape cannot mix sparse and dense dimensions; "
                     f"got shape={mat.shape} new_shape={new_sizes} with n_dense={mat.n_dense}")

  i1 = cuml_shape.searchsorted(batch_size, side='right')
  i2 = cuml_shape.searchsorted(batch_size * sparse_size, side='right')
  new_batch_shape, new_sparse_shape, new_dense_shape = split_list(new_sizes, [int(i1), int(i2)])

  # Reshape batch & dense dimensions: this is accomplished via a standard reshape.
  data = lax.reshape(
    mat.data, new_sizes=(*new_batch_shape, mat.nse, *new_dense_shape),
    dimensions=(*batch_perm, mat.n_batch, *(p + mat.n_batch + 1 for p in dense_perm)))
  indices = lax.reshape(
    mat.indices, new_sizes=(*new_batch_shape, mat.nse, mat.n_sparse),
    dimensions=(*batch_perm, mat.n_batch, mat.n_batch + 1))

  # Reshape the sparse dimensions: this is accomplished by re-indexing.
  if not new_sparse_shape:
    indices = jnp.zeros_like(indices, shape=(*new_batch_shape, mat.nse, 0))
  elif sparse_shape:
    index_cols = tuple(indices[..., i] for i in sparse_perm)
    sparse_shape = [int(mat.shape[mat.n_batch + i]) for i in sparse_perm]
    flat_indices = jnp.ravel_multi_index(index_cols, dims=tuple(sparse_shape), mode='clip')
    with jax.numpy_rank_promotion('allow'):
      oob_indices = (indices >= jnp.array(mat.shape[mat.n_batch: mat.n_batch + mat.n_sparse],
                                          dtype=indices.dtype)).any(-1, keepdims=True)
    new_index_cols = jnp.unravel_index(flat_indices, new_sparse_shape)
    indices = jnp.concatenate([col[..., None] for col in new_index_cols], axis=-1)
    indices = jnp.where(oob_indices, jnp.array(new_sparse_shape, dtype=indices.dtype), indices)

  return BCOO((data, indices), shape=new_sizes)

