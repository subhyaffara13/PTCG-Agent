import math


def bcoo_update_layout(mat: BCOO, *, n_batch: int | None = None, n_dense: int | None = None,
                       on_inefficient: str | None = 'error') -> BCOO:
  """Update the storage layout (i.e. n_batch & n_dense) of a BCOO matrix.

  In many cases this can be done without introducing undue storage overhead. However,
  increasing ``mat.n_batch`` or ``mat.n_dense`` will lead to very inefficient storage,
  with many explicitly-stored zeros, unless the new batch or dense dimensions have size
  0 or 1. In such cases, ``bcoo_update_layout`` will raise a :class:`SparseEfficiencyError`.
  This can be silenced by specifying the ``on_inefficient`` argument.

  Args:
    mat : BCOO array
    n_batch : optional(int) the number of batch dimensions in the output matrix. If None,
      then n_batch = mat.n_batch.
    n_dense : optional(int) the number of dense dimensions in the output matrix. If None,
      then n_dense = mat.n_dense.
    on_inefficient : optional(string), one of ``['error', 'warn', None]``. Specify the
      behavior in case of an inefficient reconfiguration. This is defined as a reconfiguration
      where the size of the resulting representation is much larger than the size of the
      input representation.

  Returns:
    mat_out : BCOO array
      A BCOO array representing the same sparse array as the input, with the specified
      layout. ``mat_out.todense()`` will match ``mat.todense()`` up to appropriate precision.
  """
  # TODO(jakevdp): allow specification of nse?
  # TODO(jakevdp): there is room for some improvements here:
  # - we could probably do better in the case of converting a dense dim to
  #   a batch dim or vice-versa. Worth adding that special case?
  # - we could work to preserve broadcasted batch dimensions when possible.
  # - if indices are known to be unique, we can convert them to batch/dense
  #   dimensions more efficiently.
  n_batch = mat.n_batch if n_batch is None else operator.index(n_batch)
  n_dense = mat.n_dense if n_dense is None else operator.index(n_dense)

  if (n_batch, n_dense) == (mat.n_batch, mat.n_dense):
    return mat

  n_sparse = mat.ndim - n_batch - n_dense
  if on_inefficient not in ['error', 'warn', None]:
    raise ValueError("on_inefficent={on_inefficient!r}; expected one of ['error', 'warn', None].")

  if n_batch < 0:
    raise ValueError(f"n_batch must be non-negative; got {n_batch}")
  if n_dense < 0:
    raise ValueError(f"n_dense must be non-negative; got {n_dense}")
  if n_sparse < 0:
    raise ValueError(f"sum of {n_batch=} and {n_dense=} "
                     f"cannot be larger than mat.ndim={mat.ndim}.")

  def _maybe_err_or_warn(msg):
    if on_inefficient == 'error':
      msg += (" To disable this error, set the on_inefficient argument "
              "of bcoo_update_layout to 'warn' or None.")
      raise SparseEfficiencyError(msg)
    elif on_inefficient == 'warn':
      msg += (" To disable this warning, set the on_inefficient argument "
              "of bcoo_update_layout to None.")
      warnings.warn(msg, category=SparseEfficiencyWarning)

  # TODO(jakevdp): are efficiency warnings necessary when nse is 0 or 1?
  if (n_dense > mat.n_dense and
      any(d > 1 for d in mat.shape[-n_dense:mat.ndim - mat.n_dense])):
    _maybe_err_or_warn(f"For matrix of shape {mat.shape}, increasing n_dense from "
                       f"{mat.n_dense} to {n_dense} results in inefficient storage.")
  if n_batch > mat.n_batch and any(d > 1 for d in mat.shape[mat.n_batch:n_batch]):
    _maybe_err_or_warn(f"For matrix of shape {mat.shape}, increasing n_batch from "
                       f"{mat.n_batch} to {n_batch} results in inefficient storage.")

  new_data, new_indices = mat.data, mat.indices
  shape = mat.shape
  current_n_batch = mat.n_batch
  current_n_dense = mat.n_dense

  if n_dense < current_n_dense:
    n = current_n_dense - n_dense
    @partial(nfold_vmap, N=current_n_batch + 1)
    def _update(d, i):
      new_d = d.reshape(math.prod(d.shape[:n]), *d.shape[n:])
      meshes = jnp.meshgrid(*(jnp.arange(s, dtype=i.dtype) for s in d.shape[:n]),
                            indexing='ij')
      new_i = jnp.column_stack([jnp.broadcast_to(i, (new_d.shape[0], i.size)),
                                *map(jnp.ravel, meshes)])
      return new_d, new_i
    new_data, new_indices = _update(new_data, new_indices)
    new_data = new_data.reshape(*new_data.shape[:current_n_batch],
                                math.prod(new_data.shape[current_n_batch:current_n_batch + 2]),
                                *new_data.shape[current_n_batch + 2:])
    new_indices = new_indices.reshape(*new_indices.shape[:current_n_batch],
                                      math.prod(new_indices.shape[current_n_batch: current_n_batch + 2]),
                                      *new_indices.shape[current_n_batch + 2:])
    current_n_dense = n_dense

  if n_batch < current_n_batch:
    n = current_n_batch - n_batch
    @partial(nfold_vmap, N=n_batch)
    def _update(d, i):
      nse = i.shape[-2]
      new_d = d.reshape(math.prod(d.shape[:n + 1]), *d.shape[n + 1:])
      meshes = jnp.meshgrid(*(jnp.arange(d, dtype=i.dtype) for d in (*i.shape[:n], nse)),
                            indexing='ij')
      new_i = i.reshape(math.prod(i.shape[:n + 1]), *i.shape[n + 1:])
      new_i = jnp.column_stack((*(m.ravel() for m in meshes[:-1]), new_i))
      return new_d, new_i
    new_data, new_indices = _update(new_data, new_indices)
    current_n_batch = n_batch

  if n_dense > current_n_dense:
    n = n_dense - current_n_dense
    @partial(nfold_vmap, N=current_n_batch + 1)
    def _update(d, i):
      new_d = jnp.zeros_like(d, shape=shape[-n_dense:]).at[tuple(i[-n:])].set(d)
      new_i = i[:-n]
      return new_d, new_i
    new_data, new_indices = _update(new_data, new_indices)
    current_n_dense = n_dense

  if n_batch > current_n_batch:
    n = n_batch - current_n_batch
    @partial(nfold_vmap, N=current_n_batch)
    def _update(d, i):
      nse = i.shape[-2]
      idx = tuple(i[:, j] for j in range(n)) + (jnp.arange(nse),)
      new_i_shape = (*shape[current_n_batch:n_batch], nse, i.shape[-1] - n)
      new_i = jnp.broadcast_to(i[:, n:], new_i_shape)
      new_d_shape = (*shape[current_n_batch:n_batch], nse, *d.shape[d.ndim - n_dense:])
      new_d = jnp.zeros_like(d, shape=new_d_shape).at[idx].set(d)
      return new_d, new_i
    new_data, new_indices = _update(new_data, new_indices)
    current_n_batch = n_batch

  return BCOO((new_data, new_indices), shape=shape)

