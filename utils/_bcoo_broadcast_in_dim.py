import math


def _bcoo_broadcast_in_dim(data: Array, indices: Array, *, spinfo: SparseInfo, shape: Shape,
                           broadcast_dimensions: Sequence[int]) -> tuple[Array, Array]:
  """BCOO equivalent of lax.broadcast_in_dim"""
  if len(spinfo.shape) != len(broadcast_dimensions):
    raise ValueError(f"{spinfo.shape=} and {broadcast_dimensions=} must have the same length")
  props = _validate_bcoo(data, indices, spinfo.shape)
  batch_dims, sparse_dims, dense_dims = split_list(broadcast_dimensions, [props.n_batch, props.n_sparse])

  if max(batch_dims, default=0) > min(sparse_dims, default=len(shape)):
    raise ValueError("Cannot mix batch and sparse dimensions during broadcast_in_dim")
  if max(sparse_dims, default=0) > min(dense_dims, default=len(shape)):
    raise ValueError("Cannot mix sparse and dense dimensions during broadcast_in_dim")

  # All new dimensions preceding a sparse or dense dimension are batch dimensions:
  new_n_batch = min(broadcast_dimensions[props.n_batch:], default=len(shape))
  # TODO(jakevdp): Should new trailing dimensions be dense by default?
  new_n_dense = props.n_dense and len(shape) - min(broadcast_dimensions[-props.n_dense:])
  new_n_sparse = len(shape) - new_n_batch - new_n_dense

  if math.prod(spinfo.shape[props.n_batch: props.n_batch + props.n_sparse]) != math.prod(shape[new_n_batch:new_n_batch + new_n_sparse]):
    raise NotImplementedError("Adding sparse dimensions with lengths != 1")
  new_data, new_indices = data, indices

  # batch & dense dimensions
  if (new_n_batch, new_n_dense) != (props.n_batch, props.n_dense):
    new_data = lax.broadcast_in_dim(new_data,
        shape=(*shape[:new_n_batch], props.nse, *shape[new_n_batch + new_n_sparse:]),
        broadcast_dimensions=(*batch_dims, new_n_batch, *(b + 1 - new_n_sparse for b in dense_dims)))
    new_indices = lax.broadcast_in_dim(new_indices,
        shape=(*shape[:new_n_batch], props.nse, props.n_sparse),
        broadcast_dimensions=(*batch_dims, new_n_batch, new_n_batch + 1))

  # sparse dimensions
  if new_n_sparse != props.n_sparse:
    shape = (*shape[:new_n_batch], props.nse, new_n_sparse)
    ind = jnp.array(sparse_dims, int) - new_n_batch
    new_indices = (jnp.zeros_like(new_indices, shape=shape).at[..., ind].set(new_indices))

  return new_data, new_indices

