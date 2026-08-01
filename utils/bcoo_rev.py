
def bcoo_rev(operand, dimensions):
  """Sparse implementation of :func:`jax.lax.rev`"""
  # Check validity of dimensions via original implementation.
  _ = jax.jit(lax.rev, static_argnames=("dimensions",)).eval_shape(
          jax.ShapeDtypeStruct(operand.shape, operand.dtype),
          dimensions=dimensions)
  batch_dims = [d for d in dimensions if d < operand.n_batch]
  sparse_dims = [d for d in dimensions if operand.n_batch <= d < operand.n_batch + operand.n_sparse]
  dense_dims = [d for d in dimensions if d >= operand.n_batch + operand.n_sparse]

  data, indices = operand.data, operand.indices

  if batch_dims:
    indices = lax.rev(indices, dimensions=batch_dims)
  if batch_dims or dense_dims:
    data = lax.rev(data, dimensions=batch_dims + [d + 1 - operand.n_sparse for d in dense_dims])

  if sparse_dims:
    sparse_shape = jnp.array(operand.shape[operand.n_batch: operand.n_batch + operand.n_sparse],
                             dtype=indices.dtype)
    spdims = jnp.array([d - operand.n_batch for d in sparse_dims])
    indices = indices.at[..., spdims].mul(-1)
    indices = indices.at[..., spdims].add(sparse_shape[spdims] - 1)
    indices = jnp.where(indices < 0, sparse_shape, indices)

  return BCOO((data, indices), shape=operand.shape)

