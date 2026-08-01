
def _searchsorted_compare_all_impl(
    sorted_arr: Array, query: Array, side: str, dtype: np.dtype
) -> Array:
  assert sorted_arr.ndim == 1
  assert side in ["left", "right"]
  op = lax._sort_lt_comparator if side == "left" else lax._sort_le_comparator
  comparisons = api.vmap(op, in_axes=(0, None))(sorted_arr, query)
  return comparisons.sum(dtype=dtype, axis=0)

