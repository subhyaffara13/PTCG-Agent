
def _bcoo_dot_general_impl(lhs_data, lhs_indices, rhs, *, dimension_numbers,
                           preferred_element_type, lhs_spinfo: SparseInfo):
  lhs_data = jnp.asarray(lhs_data)
  lhs_indices = jnp.asarray(lhs_indices)
  rhs = jnp.asarray(rhs)
  # Validate all inputs via abstract_eval
  out_aval = _bcoo_dot_general_abstract_eval(lhs_data.aval, lhs_indices.aval, rhs.aval,
                                             dimension_numbers=dimension_numbers,
                                             preferred_element_type=preferred_element_type,
                                             lhs_spinfo=lhs_spinfo)
  n_sparse = lhs_indices.shape[-1]
  n_batch = lhs_indices.ndim - 2

  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_contracting_b, rhs_contracting_b = unzip2([
    (l, r) for l, r in safe_zip(lhs_contracting, rhs_contracting) if l < n_batch])
  lhs_contracting_s, rhs_contracting_s = unzip2([
    (l, r) for l, r in safe_zip(lhs_contracting, rhs_contracting) if l >= n_batch])

  # Reorder lhs batch dimensions
  if lhs_batch or lhs_contracting_b:
    batch_perm = [*lhs_batch, *remaining(range(n_batch), lhs_batch, lhs_contracting_b), *lhs_contracting_b]
    lhs_data = lhs_data.transpose([*batch_perm, *range(n_batch, lhs_data.ndim)])
    lhs_indices = lhs_indices.transpose([*batch_perm, *range(n_batch, lhs_indices.ndim)])

  # Reorder lhs sparse dimensions
  if lhs_contracting_s:
    lhs_contracting_s = tuple(d - n_batch for d in lhs_contracting_s)
    sparse_perm = jnp.array([*lhs_contracting_s, *remaining(range(n_sparse), lhs_contracting_s)])
    lhs_indices = lhs_indices[..., sparse_perm]

  # Reorder rhs dimensions
  rhs_perm = [*rhs_batch, *rhs_contracting_b, *rhs_contracting_s,
              *remaining(range(rhs.ndim), rhs_batch, rhs_contracting)]
  rhs = rhs.transpose(rhs_perm)

  def result(out_array, lhs_data, lhs_indices, rhs):
    idx = tuple(lhs_indices[..., i] for i in range(n_sparse))
    idx_right = idx[:len(lhs_contracting_s)]
    idx_out = idx[len(lhs_contracting_s):]
    if idx_right and lhs_indices.ndim > 2:
      idx_batch = jnp.meshgrid(
          *(jnp.arange(n) for n in lhs_indices.shape[:-1]),
          indexing='ij')[:lhs_indices.ndim - 2]
      idx_right = (*idx_batch, *idx_right)
    batch_dims = list(range(len(lhs_contracting_b) + bool(lhs_contracting_s)))
    prod = lax.dot_general(lhs_data, rhs.at[idx_right].get(mode='fill', fill_value=0),
                           (([], []), (batch_dims, batch_dims)),
                           preferred_element_type=preferred_element_type)
    if idx_out:
      return out_array.at[idx_out].add(prod)
    else:
      return prod.sum(tuple(range(prod.ndim - out_array.ndim)), dtype=out_array.dtype)
  result = nfold_vmap(result, n_batch - len(lhs_contracting_b))
  rhs = lax.expand_dims(rhs, range(len(rhs_batch), n_batch - len(lhs_contracting_b)))
  out_array = jnp.zeros(out_aval.shape, out_aval.dtype)
  return result(out_array, lhs_data, lhs_indices, rhs)

