
def _generic_lu_pivots_to_permutation(swaps, permutation_size):
  """Converts the pivots (row swaps) returned by LU to a permutation.

  We build a permutation rather than applying `swaps` directly to the rows
  of a matrix because lax loops aren't differentiable.

  Args:
    swaps: an array of shape (..., k) of row swaps to perform
    permutation_size: the size of the output permutation. Should be >= k.
  Returns:
    An int32 array of shape (..., m).
  """
  assert len(swaps.shape) >= 1
  batch_dims = swaps.shape[:-1]
  swaps_sharding = core.typeof(swaps).sharding
  batch_spec = swaps_sharding.spec[:-1]
  if swaps_sharding.spec[-1] != None:
    raise ValueError(
        "The last dim of swaps should be unsharded but got:"
        f" {swaps_sharding.spec[-1]} for type {core.typeof(swaps)}")
  permutation_sharding = swaps_sharding.update(spec=batch_spec + (None,))
  k = swaps.shape[-1]
  m = permutation_size

  permutation = lax.broadcasted_iota(
      np.int32, batch_dims + (m,), len(batch_dims),
      out_sharding=permutation_sharding)
  if m == 0 or k == 0:
    return permutation
  upper = np.array(k, np.int32) if is_constant_dim(k) else k
  permutation, swaps = core.auto_insert_reshard(permutation, swaps)
  result, _ = control_flow.fori_loop(np.array(0, np.int32), upper,
                                     _lu_pivots_body_fn, (permutation, swaps))
  return result

