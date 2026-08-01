
def _searchsorted_scan_impl(
    sorted_arr: Array, query: Array, side: str, dtype: np.dtype, unrolled: bool
) -> Array:
  """Scan-based implementation of searchsorted."""
  assert sorted_arr.ndim == 1
  assert side in ["left", "right"]
  (n,) = sorted_arr.shape
  if sorted_arr.size == 0:
    return lax.full(query.shape, fill_value=0, dtype=dtype)
  if query.ndim > 0:
    return api.vmap(
        functools.partial(_searchsorted_scan_impl, side=side, dtype=dtype, unrolled=unrolled),
        in_axes=(None, 0),
    )(sorted_arr, query)

  op = lax._sort_le_comparator if side == "left" else lax._sort_lt_comparator
  unsigned_dtype = np.uint64 if dtypes.iinfo(dtype).bits == 64 else np.uint32
  def body_fun(state, _):
    low, high = state
    mid = low + (high - low) // 2  # use this form to avoid overflow
    go_left = op(query, sorted_arr[mid])
    return (lax.select(go_left, low, mid), lax.select(go_left, mid, high)), ()
  n_levels = int(np.ceil(np.log2(n + 1)))
  vma = tuple(core.typeof(sorted_arr).mat.varying)
  init = (core.pvary(unsigned_dtype(0), vma), core.pvary(unsigned_dtype(n), vma))
  carry, _ = control_flow.scan(body_fun, init, (), length=n_levels,
                               unroll=n_levels if unrolled else 1)
  return carry[1].astype(dtype)

