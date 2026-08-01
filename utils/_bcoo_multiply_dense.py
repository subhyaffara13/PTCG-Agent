
def _bcoo_multiply_dense(data: Array, indices: Array, v: Array, *, spinfo: SparseInfo) -> Array:
  """Broadcasted elementwise multiplication between a BCOO array and a dense array."""
  # TODO(jakevdp): the logic here is similar to bcoo_extract... can we reuse that?
  shape = spinfo.shape
  if v.ndim == 0:
    return lax.mul(data, v)
  if shape == v.shape:
    # Note: due to distributive property, no deduplication necessary!
    return lax.mul(data, _bcoo_extract(indices, v))

  if lax.broadcast_shapes(v.shape, shape) != shape:
    raise NotImplementedError(
      "multiplication between sparse and dense is only implemented for cases "
      "where the output shape matches the sparse matrix shape. Got "
      f"{shape=}, {v.shape=}")
  v = lax.expand_dims(v, range(len(shape) - v.ndim))

  props = _validate_bcoo(data, indices, shape)

  @partial(nfold_vmap, N=props.n_batch)
  def _mul(data, indices, v):
    assert indices.shape[1] == v.ndim - props.n_dense
    ind = tuple(indices[:, i] for i in range(indices.shape[1]))
    ind = tuple(i if s != 1 else 0 for i, s in zip(ind, v.shape))
    return data * v[ind]
  return _mul(data, indices, v)

