
def bcoo_concatenate(operands: Sequence[BCOO], *, dimension: int) -> BCOO:
  """Sparse implementation of :func:`jax.lax.concatenate`

  Args:
    operands : Sequence of BCOO arrays to concatenate. The arrays must have equal
      shapes, except in the `dimension` axis. Additionally, the arrays must have
      have equivalent batch, sparse, and dense dimensions.
    dimension : Positive integer specifying the dimension along which to concatenate
      the arrays. The dimension must be among batch or sparse dimensions of the input;
      concatenation along dense dimensions is not supported.

  Returns:
    A BCOO array containing the concatenation of the inputs.
  """
  dimension = operator.index(dimension)
  if not all(isinstance(op, BCOO) for op in operands):
    raise ValueError("bcoo_concatenate: expected operands to be a sequence of BCOO arrays. "
                     f"Got {operands}")
  # Validate inputs using lax.concatenate abstract evaluation.
  out_aval = jax.jit(lax.concatenate, static_argnames=("dimension",)).eval_shape(
          [core.ShapedArray(op.shape, op.dtype) for op in operands],
          dimension=dimension)
  if len({op.n_dense for op in operands}) > 1:
    raise ValueError("bcoo_concatenate requires inputs to have matching nse dimensions.")

  n_batches = {op.n_batch for op in operands}
  # Correct for the common case, where op[None, :] adds a single batch dimension and we
  # need to align it in order to match the others & concatenate.
  if len(n_batches) != 1 and max(n_batches) == 1:
    if all(op.shape[0] == 1 for op in operands if op.n_batch == 0):
      operands = [bcoo_update_layout(op, n_batch=1) if op.n_batch == 0 else op for op in operands]
    elif all(op.shape[0] == 1 for op in operands if op.n_batch == 1):
      operands = [bcoo_update_layout(op, n_batch=0) if op.n_batch == 1 else op for op in operands]
    n_batches = {op.n_batch for op in operands}

  if len(n_batches) != 1:
    raise ValueError("bcoo_concatenate requires inputs to have matching batch dimensions.")

  n_batch, n_sparse = operands[0].n_batch, operands[0].n_sparse

  index_batches = [op.indices.shape[:n_batch] for op in operands]
  data_batches = [op.data.shape[:n_batch] for op in operands]
  if dimension < n_batch:
    index_batches = [s[:dimension] + s[dimension + 1:] for s in index_batches]
    data_batches = [s[:dimension] + s[dimension + 1:] for s in data_batches]
  if not (len(set(index_batches)) == len(set(data_batches)) == 1):
    raise NotImplementedError("concatenation of arrays with broadcasted batch indices")

  if dimension < n_batch:  # Concatenation along batch axes
    # Ensure nse of operands match.
    nses = {op.nse for op in operands}
    if len(nses) != 1:
      nse = max(nses)
      operands = [_bcoo_set_nse(op, nse) for op in operands]
    new_indices = lax.concatenate([op.indices for op in operands], dimension=dimension)
    new_data = lax.concatenate([op.data for op in operands], dimension=dimension)
  elif dimension < n_batch + n_sparse:  # Concatenation along sparse axes
    offsets = np.cumsum([0] + [op.shape[dimension] for op in operands[:-1]],
                        dtype=operands[0].indices.dtype)
    new_data = lax.concatenate([op.data for op in operands], dimension=n_batch)
    new_indices = lax.concatenate([op.indices.at[..., dimension - n_batch].add(offset)
                                   for op, offset in safe_zip(operands, offsets)],
                                  dimension=n_batch)
  else:  # Concatenation along dense axes
    # TODO(jakevdp) should we implement this? In general it results in a wasteful
    # representation because we cannot assume that the indices match.
    raise NotImplementedError("Concatenation along dense dimensions.")

  return BCOO((new_data, new_indices), shape=out_aval.shape)

