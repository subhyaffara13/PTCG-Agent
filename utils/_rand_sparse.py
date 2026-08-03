from typing import Any, Callable

def _rand_sparse(shape: Sequence[int], dtype: DTypeLike, *,
                 rng: np.random.RandomState, rand_method: Callable[..., Any],
                 nse: int | float, n_batch: int, n_dense: int,
                 sparse_format: str) -> sparse.BCOO | sparse.BCSR:
  if sparse_format not in ['bcoo', 'bcsr']:
    raise ValueError(f"Sparse format {sparse_format} not supported.")

  n_sparse = len(shape) - n_batch - n_dense

  if n_sparse < 0 or n_batch < 0 or n_dense < 0:
    raise ValueError(f"Invalid parameters: {shape=} {n_batch=} {n_sparse=}")

  if sparse_format == 'bcsr' and n_sparse != 2:
    raise ValueError("bcsr array must have 2 sparse dimensions; "
                     f"{n_sparse} is given.")

  batch_shape, sparse_shape, dense_shape = split_list(shape,
                                                      [n_batch, n_sparse])
  if 0 <= nse < 1:
    nse = int(np.ceil(nse * np.prod(sparse_shape)))
  nse_int = int(nse)
  data_rng = rand_method(rng)
  data_shape = (*batch_shape, nse_int, *dense_shape)
  data = jnp.array(data_rng(data_shape, dtype))

  int32 = np.dtype('int32')
  if sparse_format == 'bcoo':
    index_shape = (*batch_shape, nse_int, n_sparse)
    indices = jnp.array(
      rng.randint(0, sparse_shape, size=index_shape, dtype=int32))
    return sparse.BCOO((data, indices), shape=shape)
  else:
    index_shape = (*batch_shape, nse_int)
    indptr_shape = (*batch_shape, sparse_shape[0] + 1)
    indices = jnp.array(
      rng.randint(0, sparse_shape[1], size=index_shape, dtype=int32))
    indptr = jnp.sort(
      rng.randint(0, nse_int + 1, size=indptr_shape, dtype=int32), axis=-1)
    indptr = indptr.at[..., 0].set(0)
    return sparse.BCSR((data, indices, indptr), shape=shape)

