
def _bcoo_dot_general_sampled_simple2(A, B, indices, *, dimension_numbers, precision):
  # This case used in transpose of sparse matmat
  # TODO(jakevdp) generalize this
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  assert not (lhs_batch or rhs_batch)
  assert len(lhs_contract) == len(rhs_contract) == 1
  assert A.ndim == B.ndim == 2
  n_batch = indices.ndim - 2
  n_sparse = indices.shape[-1]
  nse = indices.shape[-2]
  assert n_batch + n_sparse == 2
  if n_batch == 0:
    lhs_batch = [1] if lhs_contract[0] == 0 else [0]
    rhs_batch = [1] if rhs_contract[0] == 0 else [0]
    A = A.at[_tuple_replace((slice(None), slice(None)), lhs_batch[0], indices[:, 0])].get(mode='fill', fill_value=0)
    B = B.at[_tuple_replace((slice(None), slice(None)), rhs_batch[0], indices[:, 1])].get(mode='fill', fill_value=0)
    return lax.dot_general(A, B, dimension_numbers=((lhs_contract, rhs_contract), (lhs_batch, rhs_batch)),
                           precision=precision)
  if n_batch == 1:
    lhs_batch = [1] if lhs_contract[0] == 0 else [0]
    rhs_batch = [1] if rhs_contract[0] == 0 else [0]
    B = B.at[_tuple_replace((slice(None), slice(None)), rhs_batch[0], indices[..., 0])].get(mode='fill', fill_value=0)
    if rhs_contract[0] == 1:
      rhs_contract = [2]
    return lax.dot_general(A, B, dimension_numbers=((lhs_contract, rhs_contract), (lhs_batch, rhs_batch)),
                           precision=precision)
  if n_batch == 2:
    out = lax.dot_general(A, B, dimension_numbers=((lhs_contract, rhs_contract), (lhs_batch, rhs_batch)),
                          precision=precision)
    return lax.broadcast_in_dim(lax.expand_dims(out, (2,)), (*out.shape, nse), (0, 1, 2))
  else:
    raise ValueError("too many batch dimensions.")

