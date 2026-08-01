
def _ensure_batch_dim(lhs, rhs, dimension_numbers):
  contracting_dims, (lhs_batch, rhs_batch) = dimension_numbers
  lhs_batched = lhs
  rhs_batched = rhs

  if lhs_batch == ():  # expand the last dim
    lhs_batched = jnp.expand_dims(lhs, axis=lhs.aval.ndim)
    lhs_batch = (lhs.aval.ndim,)
  if rhs_batch == ():
    rhs_batched = jnp.expand_dims(rhs, axis=rhs.aval.ndim)
    rhs_batch = (rhs.aval.ndim,)
  dn_batched = contracting_dims, (lhs_batch, rhs_batch)
  return lhs_batched, rhs_batched, dn_batched

