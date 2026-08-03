import functools

def _bcsr_rewriting_take(arr, idx, indices_are_sorted=False, unique_indices=False,
                           mode=None, fill_value=None):
  # Only sparsify the array argument; sparse indices not yet supported
  result = sparsify(functools.partial(
    jnp_indexing.rewriting_take, idx=idx, indices_are_sorted=indices_are_sorted,
    mode=mode, unique_indices=unique_indices, fill_value=fill_value))(arr)
  return result

