
def _bcoo_dot_general_sampled_simple(A, B, indices, *, dimension_numbers, precision):
  # This case used in transpose of sparse matvec
  # TODO(jakevdp) generalize this
  del precision  # Unused here
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  assert not (lhs_contract or rhs_contract or lhs_batch or rhs_batch)
  assert A.ndim == B.ndim == 1
  n_batch = indices.ndim - 2
  n_sparse = indices.shape[-1]
  nse = indices.shape[-2]
  assert n_batch + n_sparse == 2
  if n_batch == 0:
    return (A.at[indices[:, 0]].get(mode='fill', fill_value=0)
            * B.at[indices[:, 1]].get(mode='fill', fill_value=0))
  elif n_batch == 1:
    return A[:, None] * B.at[indices[..., 0]].get(mode='fill', fill_value=0)
  elif n_batch == 2:
    out = A[:, None, None] * B[None, :, None]
    return lax.broadcast_in_dim(out, (len(A), len(B), nse), (0, 1, 2))
  else:
    raise ValueError("too many batch dimensions.")

