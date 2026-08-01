
def _searchsorted_sort_impl(
    sorted_arr: Array, query: Array, side: str, dtype: np.dtype
) -> Array:
  """Cosorting-based implementation of searchsorted."""
  assert sorted_arr.ndim == 1
  assert side in ["left", "right"]
  working_dtype = (
      np.int32
      if sorted_arr.size + query.size <= np.iinfo(np.int32).max
      else np.int64
  )

  def _rank(x):
    idx = lax.iota(working_dtype, len(x))
    return lax.full_like(idx, 0).at[lax.sort_key_val(x, idx)[1]].set(idx)

  if side == "left":
    index = _rank(lax.concatenate([query.ravel(), sorted_arr], 0))[: query.size]
  else:
    index = _rank(lax.concatenate([sorted_arr, query.ravel()], 0))[
        sorted_arr.size :
    ]
  return lax.reshape(
      lax.sub(index, _rank(query.ravel())), np.shape(query)
  ).astype(dtype)

