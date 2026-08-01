
def _spsolve_abstract_eval(data, indices, indptr, b, *, tol, reorder):
  if data.dtype != b.dtype:
    raise ValueError(f"data types do not match: {data.dtype=} {b.dtype=}")
  if not (jnp.issubdtype(indices.dtype, jnp.integer) and jnp.issubdtype(indptr.dtype, jnp.integer)):
    raise ValueError(f"index arrays must be integer typed; got {indices.dtype=} {indptr.dtype=}")
  if not data.ndim == indices.ndim == indptr.ndim == b.ndim == 1:
    raise ValueError("Arrays must be one-dimensional. "
                     f"Got {data.shape=} {indices.shape=} {indptr.shape=} {b.shape=}")
  if indptr.size != b.size + 1 or  data.shape != indices.shape:
    raise ValueError(f"Invalid CSR buffer sizes: {data.shape=} {indices.shape=} {indptr.shape=}")
  if reorder not in [0, 1, 2, 3]:
    raise ValueError(f"{reorder=} not valid, must be one of [1, 2, 3, 4]")
  tol = float(tol)
  return b

