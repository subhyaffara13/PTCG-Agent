
def _coo_correct_out_of_bound_indices(row, col, shape, transpose):
  # Since cusparse does not have any well-tested support for padded indices,
  # we push them into an extra row/col of the matrix, which will then be
  # sliced away in the output.
  assert row.ndim == col.ndim, f"{row.ndim} != {col.ndim}"
  assert len(shape) == row.ndim + 1, f"{len(shape)} != {row.ndim + 1}"
  if row.ndim > 1:
    f = partial(_coo_correct_out_of_bound_indices,
                shape=shape[row.ndim:], transpose=transpose)
    return nfold_vmap(f, row.ndim)(row, col)
  mask = (row >= shape[0]) | (col >= shape[1])
  if transpose:
    row = jnp.where(mask, 0, row)
    col = jnp.where(mask, shape[1], col)
    shape = (shape[0], shape[1] + 1)
  else:
    row = jnp.where(mask, shape[0], row)
    col = jnp.where(mask, 0, col)
    shape = (shape[0] + 1, shape[1])
  return row, col, shape

